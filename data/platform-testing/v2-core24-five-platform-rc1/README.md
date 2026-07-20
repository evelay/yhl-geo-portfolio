# v2-core24 five-platform rc1 testing templates

This directory prepares the approved v2-core24-rc1 manual collection templates for the five-platform main set.

## Scope

- Run ID: V2-CORE24-FIVE-R1
- Question set version: v2-core24-rc1
- Question count: 24
- Main platforms: doubao, wenxin, qwen, kimi, yuanbao
- Expected response rows: 24 questions x 5 platforms = 120
- Collection method: manual-copy
- Run status: template-ready-not-started

## Platform Governance

The main platform set is fixed to 豆包, 文心一言, 通义千问, Kimi, and 腾讯元宝. ChatGPT and DeepSeek are supplementary-platform-candidate only for this stage and have no response collection rows in the main templates.

## Files

- core24-test-plan.csv: approved question-level test plan copied from core24, including the 08D2 q20 risk_level adjustment to medium.
- five-platform-response-template.csv: 120 empty answer collection rows, one per question-platform pair.
- human-score-template.csv: 120 empty human scoring rows, matched one-to-one with response_id.
- test-run-registry.csv: one registry row for V2-CORE24-FIVE-R1.
- source-link-template.csv: empty visible-source capture rows keyed by response_id.
- historical-baseline-mapping.csv: Baseline150 mapping scaffold that preserves historical separation and flags missing raw response references for manual review.

## Collection Rules

Do not call any platform from this template stage. Do not generate simulated answers. Keep raw_answer and visible_source_urls blank until a human collector copies real platform output. Blank answers are not zero scores and must remain not-collected until actual collection occurs.

## Baseline Boundary

Baseline150 remains a historical five-platform baseline: 30 questions x 5 platforms = 150 historical answers. The historical sample must not be merged with V2-CORE24-FIVE-R1 into an undated aggregate metric. Different collection dates, model versions, and unrecorded search modes must remain explicit comparison limits.
