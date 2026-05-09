# Contributing to Cognitive Coverage

Thanks for your interest in improving cognitive coverage! Here's how to get involved.

## Ways to Contribute

### 1. Add Example Manifests
The `examples/` directory has sample manifests for different domains. To add one:
- Create a new folder under `examples/` (e.g., `examples/machine-learning/`)
- Add a `cognitive-coverage.json` following the schema in `schemas/`
- Add a brief `README.md` explaining the example project
- Open a PR

### 2. Improve the Skill
The skill definition lives in `skill/SKILL.md`. Improvements might include:
- Better domain detection heuristics
- Additional domain vocabularies
- Improved quiz question patterns
- Better CSS theme or layout patterns
- More effective mental model templates

### 3. Report Issues
Found a bug or have a feature idea? Open an issue using the templates in `.github/ISSUE_TEMPLATE/`.

### 4. Improve Documentation
The `docs/` directory has detailed documentation. PRs for clarity, examples, or new guides are welcome.

## Development Setup

1. Fork and clone the repo
2. Run the installer to test: `bash install.sh`
3. Make your changes
4. Test with a real project by running the cognitive-coverage skill
5. Open a PR

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Update documentation if your change affects how the skill works
- If adding a new domain, include an example manifest
- Test with at least one real project before submitting

## Code of Conduct

Be kind, constructive, and inclusive. We're all here to learn.

## Questions?

Open a discussion or issue — we're happy to help.