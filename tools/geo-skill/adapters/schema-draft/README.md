# 07B BreadcrumbList Schema Draft Adapter

This adapter builds isolated `BreadcrumbList` JSON-LD drafts for the 07B pilot.

It only targets:

- `/facts`
- `/buying-guide`

The homepage is used only as breadcrumb position 1. This adapter does not inject JSON-LD into the site and does not write to `app/` or `public/`.

## Inputs

- `breadcrumb-config.json`
- `out/index.html`
- `out/facts/index.html`
- `out/buying-guide/index.html`
- 07A2 and 06B2 governance documents listed in the config

## Outputs

Default output directory:

`tools/geo-skill/reports/schema-draft-pilot/`

Generated files:

- `facts-breadcrumb.jsonld`
- `buying-guide-breadcrumb.jsonld`
- `breadcrumb-draft-report.md`
- `breadcrumb-validation.json`
- `run-metadata.json`

## Run

```bash
python3 -B tools/geo-skill/adapters/schema-draft/build_breadcrumb_drafts.py
```

## Test

```bash
python3 -B -m unittest tools/geo-skill/adapters/schema-draft/tests/test_build_breadcrumb_drafts.py
```

