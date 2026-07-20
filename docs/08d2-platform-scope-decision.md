# 08D2 Platform Scope Decision

Date: 2026-07-20
Decision status: approved

## Decision

Baseline150 uses the five-platform main set: 豆包, 文心一言, 通义千问, Kimi, and 腾讯元宝. It represents 30 questions x 5 platforms = 150 historical answers.

The v2-core24 main test continues with the same five-platform main set. The approved platform codes are doubao, wenxin, qwen, kimi, and yuanbao.

ChatGPT and DeepSeek are supplementary-platform-candidate for future separate testing. They are not part of the current main sample and no 08D2 response collection rows are created for them.

Earlier three-platform results are classified as early-experiment. They must not replace the current five-platform main baseline and must not be mixed into five-platform summary metrics.

## Governance Rules

Different platform groups must not be combined into one average metric.

Manual collection is the collection method, not the platform scope.

The five-platform main sample will be used for formal portfolio comparison after real collection and human scoring are complete.

Supplementary platforms must be reported independently in the future, with their own sample scope, dates, model metadata, and comparison limits.

## Current Stage Boundary

This stage approves templates only. It does not start platform testing, does not collect answers, does not score answers, and does not switch the website to consume v2.
