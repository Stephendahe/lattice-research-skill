---
name: lattice-honesty
description: >-
  Use this child skill of Lattice Research Skill when the user asks for “Lattice Honesty”, honesty review, evidence-bound audit, uncertainty audit, self-review, overclaim detection, unsupported claim removal, or honesty_score. It checks whether claims are supported by provided evidence, whether missing full text is acknowledged, and whether facts, inferences, suggestions, and unverified points are separated.
---

# Lattice Honesty

## Purpose

Use this skill to keep Lattice Research Skill outputs honest, bounded, and traceable. It is a child skill of Lattice Research Skill, but can also be used independently on reports, literature reviews, proposal drafts, and answer drafts.

Read `references/HONESTY_RULES.md` before auditing.

## Core Rule

Unknown is an acceptable output. Evidence gaps must be named, not hidden.

Never turn abstracts into full-text conclusions, correlations into causation, missing variables into controlled variables, or unverified claims into facts.

## Workflow

1. Read the target answer/report/draft.
2. Identify claims that require support:
   - factual claims;
   - numerical values;
   - mechanism claims;
   - novelty/research-gap claims;
   - experimental-method claims;
   - comparisons across papers.
3. Check whether each claim has explicit support in the user's material, tool output, file, citation, or clearly stated inference.
4. Downgrade, remove, or label unsupported claims.
5. Add or strengthen uncertainty language where needed.
6. Optionally run `scripts/score_honesty.py` on a text/Markdown file.

## Output Format

Respond in Chinese by default.

Use this table for problems:

| 原文/主张 | 问题 | 风险 | 建议处理 |
|---|---|---|---|

Then provide:

- `honesty_score`: 0-100 if enough text is available;
- `必须降级的结论`;
- `需要补证据的地方`;
- `可以保留的结论`.

## Mandatory Distinctions

Always separate:

- facts supported by evidence;
- inference from evidence;
- suggestions or next steps;
- unverified or missing information;
- tasks blocked by missing full text/data.

## Refusal / Downgrade Language

Use direct language:

- `当前材料不足，不能支持这个结论。`
- `这只能作为假设，不能写成已证明。`
- `基于摘要只能初筛，不能做实验流程审计。`
- `该比较缺少共同变量，不能强行归一化。`
- `需要全文/图表/补充材料后才能判断。`
