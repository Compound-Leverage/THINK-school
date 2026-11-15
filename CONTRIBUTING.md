# Contributing to THINK School

Thanks for helping improve the public educational Capture Team and Proposal Team packages.

## Before contributing

- Open an issue describing a bug, documentation gap, or proposed improvement before undertaking major changes.
- Keep public educational plugins distinct from proprietary Compound Leverage managed-service assets. Never submit customer data, secrets, credentials, or private documents.
- Preserve human approval gates, source verification, and bring-your-own-data behavior.
- Keep Claude Code and OpenAI Codex variants logically aligned where applicable.

## Submit a change

1. Fork the repository and create a focused branch.
2. If the change touches plugin content or metadata (skill text, icon, description, URLs, keywords), edit the relevant team's `Plugins/<team>/_source/` files only -- never hand-edit `Plugins/<team>/claude/` or `Plugins/<team>/openai/` directly. Then run `python3 scripts/build_plugins.py --write --team <name>` and commit the generated diff together with the source diff.
3. Update any other relevant documentation and examples.
4. Run `python3 scripts/validate_release.py` and `python3 scripts/check_build_drift.py`, and review the [validation checklist](Docs/plugin-validation.md).
5. Open a pull request describing what changed, how it was tested, and any limitations.

Contributions are reviewed by maintainers. Submitting a contribution does not guarantee acceptance. By contributing, you agree your submission may be distributed under the repository [LICENSE](LICENSE); only submit material you have rights to contribute.
