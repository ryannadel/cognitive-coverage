"""MCP server for Cognitive Coverage manifests."""

from __future__ import annotations

import argparse
import json
import os
import sys
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


TOOL_NAMES = (
    "list_uncovered",
    "get_concept",
    "get_flow",
    "coverage_summary",
    "find_by_file",
    "mark_status",
)

AXES = ("files", "concepts", "flows")
MANIFEST_PATH = Path.cwd() / "cognitive-coverage.json"


def configure_manifest(path: str | Path | None) -> None:
    """Set the manifest path used by tool handlers."""
    global MANIFEST_PATH
    MANIFEST_PATH = Path(path).expanduser().resolve() if path else Path.cwd() / "cognitive-coverage.json"


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")

    with MANIFEST_PATH.open("r", encoding="utf-8-sig") as manifest_file:
        data = json.load(manifest_file)

    if not isinstance(data, dict):
        raise ValueError("Manifest root must be a JSON object")

    return data


def save_manifest(manifest: dict[str, Any]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = MANIFEST_PATH.with_name(f".{MANIFEST_PATH.name}.tmp")
    payload = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"

    with tmp_path.open("w", encoding="utf-8") as manifest_file:
        manifest_file.write(payload)
        manifest_file.flush()
        os.fsync(manifest_file.fileno())

    os.replace(tmp_path, MANIFEST_PATH)


def list_uncovered(axis: str = "all") -> dict[str, Any]:
    """Return manifest items still at the first status for each axis."""
    manifest = load_manifest()
    axes = _selected_axes(axis)
    uncovered = {
        current_axis: [
            _item_summary(item, current_axis)
            for item in manifest.get(current_axis, [])
            if item.get("status") == _lowest_status(manifest, current_axis)
        ]
        for current_axis in axes
    }

    return {
        "axis": axis,
        "counts": {current_axis: len(items) for current_axis, items in uncovered.items()},
        "items": uncovered,
    }


def get_concept(concept_id: str) -> dict[str, Any]:
    """Return one concept with related file, quiz, and status data."""
    manifest = load_manifest()
    concept = _find_item(manifest, "concepts", concept_id)
    return {
        "concept": deepcopy(concept),
        "relatedFiles": concept.get("files", []),
        "quizIds": concept.get("quizIds", []),
        "status": concept.get("status"),
    }


def get_flow(flow_id: str) -> dict[str, Any]:
    """Return one flow with its steps and current status."""
    manifest = load_manifest()
    flow = _find_item(manifest, "flows", flow_id)
    return {
        "flow": deepcopy(flow),
        "steps": flow.get("steps", []),
        "quizIds": flow.get("quizIds", []),
        "status": flow.get("status"),
    }


def coverage_summary() -> dict[str, Any]:
    """Return the manifest summary plus a short natural-language synopsis."""
    manifest = load_manifest()
    summary = manifest.get("summary", {})
    project = manifest.get("project", "this project")
    domain = manifest.get("domain", "project")
    overall = summary.get("overall", 0)

    return {
        "project": project,
        "domain": domain,
        "summary": deepcopy(summary),
        "synopsis": f"{project} is {overall}% cognitively covered across its {domain} manifest.",
    }


def find_by_file(file_path: str) -> dict[str, Any]:
    """Return concepts and flows that reference a file path."""
    manifest = load_manifest()
    normalized = _normalize_path(file_path)
    files = [
        deepcopy(item)
        for item in manifest.get("files", [])
        if _normalize_path(item.get("path", "")) == normalized
    ]
    concepts = [
        deepcopy(concept)
        for concept in manifest.get("concepts", [])
        if normalized in {_normalize_path(path) for path in concept.get("files", [])}
    ]
    flows = [
        deepcopy(flow)
        for flow in manifest.get("flows", [])
        if any(_normalize_path(step.get("file", "")) == normalized for step in flow.get("steps", []))
    ]
    quiz_ids = [
        quiz_id
        for quiz_id, mapping in manifest.get("quizMapping", {}).items()
        if normalized in {_normalize_path(path) for path in mapping.get("files", [])}
    ]

    return {
        "filePath": file_path,
        "file": files[0] if files else None,
        "concepts": concepts,
        "flows": flows,
        "quizIds": quiz_ids,
    }


def mark_status(axis: str, item_id: str, status: str) -> dict[str, Any]:
    """Update one manifest item status and rewrite the manifest atomically."""
    manifest = load_manifest()
    axis = _require_axis(axis)
    allowed_statuses = manifest.get("statusLabels", {}).get(axis, [])

    if allowed_statuses and status not in allowed_statuses:
        raise ValueError(f"Status '{status}' is not valid for {axis}: {', '.join(allowed_statuses)}")

    item = _find_item(manifest, axis, item_id)
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    item["status"] = status
    item["updatedAt"] = now
    manifest["updatedAt"] = now
    _recalculate_summary(manifest)
    save_manifest(manifest)

    return {
        "axis": axis,
        "itemId": item_id,
        "status": status,
        "updatedAt": now,
        "summary": deepcopy(manifest.get("summary", {})),
    }


def build_mcp_server() -> Any:
    FastMCP = _import_fastmcp()
    mcp = FastMCP("Cognitive Coverage", json_response=True)

    @mcp.tool(name="list_uncovered")
    def list_uncovered_tool(axis: str = "all") -> dict[str, Any]:
        """List files, concepts, or flows still at their first coverage status."""
        return list_uncovered(axis)

    @mcp.tool(name="get_concept")
    def get_concept_tool(concept_id: str) -> dict[str, Any]:
        """Get a concept by id, including description, files, quiz ids, and status."""
        return get_concept(concept_id)

    @mcp.tool(name="get_flow")
    def get_flow_tool(flow_id: str) -> dict[str, Any]:
        """Get a flow by id, including steps, file references, quiz ids, and status."""
        return get_flow(flow_id)

    @mcp.tool(name="coverage_summary")
    def coverage_summary_tool() -> dict[str, Any]:
        """Get coverage summary data and a one-line synopsis."""
        return coverage_summary()

    @mcp.tool(name="find_by_file")
    def find_by_file_tool(file_path: str) -> dict[str, Any]:
        """Find manifest concepts and flows that reference a file path."""
        return find_by_file(file_path)

    @mcp.tool(name="mark_status")
    def mark_status_tool(axis: str, item_id: str, status: str) -> dict[str, Any]:
        """Update one file, concept, or flow status in the manifest."""
        return mark_status(axis, item_id, status)

    return mcp


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Serve a Cognitive Coverage manifest over MCP stdio.")
    parser.add_argument(
        "--manifest",
        default=None,
        help="Path to cognitive-coverage.json. Defaults to ./cognitive-coverage.json.",
    )
    args = parser.parse_args(argv)

    configure_manifest(args.manifest)
    build_mcp_server().run(transport="stdio")


def _selected_axes(axis: str) -> tuple[str, ...]:
    if axis == "all":
        return AXES
    return (_require_axis(axis),)


def _require_axis(axis: str) -> str:
    if axis not in AXES:
        raise ValueError(f"Axis must be one of: all, {', '.join(AXES)}")
    return axis


def _lowest_status(manifest: dict[str, Any], axis: str) -> str:
    statuses = manifest.get("statusLabels", {}).get(axis, [])
    return statuses[0] if statuses else "uncovered"


def _find_item(manifest: dict[str, Any], axis: str, item_id: str) -> dict[str, Any]:
    _require_axis(axis)
    key = "path" if axis == "files" else "id"
    normalized_id = _normalize_path(item_id) if axis == "files" else item_id

    for item in manifest.get(axis, []):
        value = _normalize_path(item.get(key, "")) if axis == "files" else item.get(key)
        if value == normalized_id:
            return item

    raise ValueError(f"No {axis[:-1]} found for '{item_id}'")


def _item_summary(item: dict[str, Any], axis: str) -> dict[str, Any]:
    key = "path" if axis == "files" else "id"
    return {
        key: item.get(key),
        "name": item.get("name"),
        "description": item.get("description"),
        "status": item.get("status"),
        "guideSection": item.get("guideSection"),
    }


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def _recalculate_summary(manifest: dict[str, Any]) -> None:
    summary: dict[str, Any] = {}
    total_items = 0
    covered_items = 0

    for axis in AXES:
        items = manifest.get(axis, [])
        lowest = _lowest_status(manifest, axis)
        total = len(items)
        covered = sum(1 for item in items if item.get("status") != lowest)
        percentage = round((covered / total) * 100) if total else 0
        summary[axis] = {"total": total, "covered": covered, "percentage": percentage}
        total_items += total
        covered_items += covered

    summary["overall"] = round((covered_items / total_items) * 100) if total_items else 0
    manifest["summary"] = summary


@contextmanager
def _without_repo_on_path() -> Iterable[None]:
    repo_root = Path(__file__).resolve().parents[1]
    cwd = Path.cwd().resolve()
    old_path = sys.path[:]
    sys.path = [
        path
        for path in sys.path
        if Path(path or cwd).resolve() != repo_root
    ]
    try:
        yield
    finally:
        sys.path = old_path


def _import_fastmcp() -> Any:
    # Running as `python -m mcp.server` shadows the SDK's `mcp.server` package.
    # Remove this repo from import resolution while loading the SDK.
    for module_name in ("mcp.server", "mcp"):
        module = sys.modules.get(module_name)
        module_file = getattr(module, "__file__", "") if module else ""
        if module_file and Path(module_file).resolve().is_relative_to(Path(__file__).resolve().parents[1]):
            sys.modules.pop(module_name, None)

    with _without_repo_on_path():
        try:
            from mcp.server.fastmcp import FastMCP
        except ImportError as exc:
            raise RuntimeError(
                "Install the MCP SDK before running the server: pip install mcp"
            ) from exc

    return FastMCP


if __name__ == "__main__":
    main()
