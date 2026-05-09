from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "mcp" / "server.py"


def load_server():
    spec = importlib.util.spec_from_file_location("cognitive_coverage_mcp_server", SERVER_PATH)
    server = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(server)
    return server


def test_tool_handlers_read_manifest_and_return_json(tmp_path):
    server = load_server()
    manifest_path = tmp_path / "cognitive-coverage.json"
    manifest_path.write_text(
        (ROOT / "examples" / "codebase" / "cognitive-coverage.json").read_text(encoding="utf-8-sig"),
        encoding="utf-8",
    )
    server.configure_manifest(manifest_path)

    assert server.TOOL_NAMES == (
        "list_uncovered",
        "list_areas",
        "get_area",
        "next_learning_targets",
        "get_concept",
        "get_flow",
        "coverage_summary",
        "find_by_file",
        "mark_status",
    )

    results = [
        server.list_uncovered(),
        server.list_areas(),
        server.get_area("security"),
        server.next_learning_targets(),
        server.get_concept("auth"),
        server.get_flow("auth-flow"),
        server.coverage_summary(),
        server.find_by_file("src/middleware/auth.ts"),
        server.mark_status("concepts", "auth", "taught"),
    ]

    for result in results:
        json.dumps(result)

    updated = json.loads(manifest_path.read_text(encoding="utf-8"))
    auth = next(concept for concept in updated["concepts"] if concept["id"] == "auth")
    assert auth["status"] == "taught"
    assert auth["updatedAt"] is not None
    assert updated["updatedAt"] == auth["updatedAt"]
    assert updated["summary"]["concepts"]["covered"] == 1
    assert not manifest_path.with_name(f".{manifest_path.name}.tmp").exists()


def test_find_by_file_returns_inverse_lookup(tmp_path):
    server = load_server()
    manifest_path = tmp_path / "cognitive-coverage.json"
    manifest_path.write_text(
        (ROOT / "examples" / "codebase" / "cognitive-coverage.json").read_text(encoding="utf-8-sig"),
        encoding="utf-8",
    )
    server.configure_manifest(manifest_path)

    result = server.find_by_file("./src/middleware/auth.ts")

    assert result["file"]["path"] == "src/middleware/auth.ts"
    assert {concept["id"] for concept in result["concepts"]} == {"auth"}
    assert {flow["id"] for flow in result["flows"]} == {"auth-flow", "crud-flow"}
    assert result["quizIds"] == ["q2", "q3", "q5"]
    assert {area["id"] for area in result["areas"]} == {"runtime", "security"}
    assert {module["id"] for module in result["modules"]} == {"api-entrypoints", "auth-boundary"}
    assert result["sourceSummary"]["path"] == "src/middleware/auth.ts"


def test_hierarchy_tools_return_area_and_learning_targets(tmp_path):
    server = load_server()
    manifest_path = tmp_path / "cognitive-coverage.json"
    manifest_path.write_text(
        (ROOT / "examples" / "codebase" / "cognitive-coverage.json").read_text(encoding="utf-8-sig"),
        encoding="utf-8",
    )
    server.configure_manifest(manifest_path)

    areas = server.list_areas()
    security = server.get_area("security")
    targets = server.next_learning_targets(limit=2)
    updated = server.mark_status("areas", "security", "mapped")

    assert {area["id"] for area in areas["areas"]} == {"runtime", "security"}
    assert security["area"]["id"] == "security"
    assert {module["id"] for module in security["modules"]} == {"auth-boundary"}
    assert {concept["id"] for concept in security["related"]["concepts"]} == {"auth"}
    assert targets["targets"][0]["id"] in {"security", "auth-boundary", "auth-flow", "auth"}
    assert updated["axis"] == "areas"
    assert updated["status"] == "mapped"
