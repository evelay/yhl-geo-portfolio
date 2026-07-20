# Question Bank Versions

This directory stores versioned question bank artifacts for the YHL GEO portfolio.

## Current Status

- Current canonical: v1, represented by `redwood_geo/data/redwood_question_bank_30.csv` outside this website repository.
- Current canonical SHA-256: `ab0661732fffc3e0aa25adabadf5d3b9c58f00baa1c5bf045f5190ebcc596936`.
- Release candidate: `v2-rc1` in `data/question-bank/redwood_question_bank_v2_rc1.csv`.
- Canonical switch status: `not-switched`.
- Website consumption status: the website must not read `v2-rc1` directly.

## Files

| File | Role |
|---|---|
| `redwood_question_bank_v2_rc1.csv` | Versioned release candidate only; not canonical. |
| `question_bank_versions.json` | Version manifest for v1 and v2-rc1. |
| `README.md` | Local governance note for this directory. |

## Rules

- Do not rename `redwood_question_bank_v2_rc1.csv` to `redwood_question_bank_30.csv`.
- Do not overwrite the external v1 canonical with this file.
- Do not wire this file into website runtime code, tests, production flows, or platform retests before final human approval.
- Keep q01-q30 unchanged and use `docs/08c-question-id-mapping.csv` for the q31-q39 candidate mapping.
