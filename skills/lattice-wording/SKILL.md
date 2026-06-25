---
name: lattice-wording
description: >-
  Use this skill for Lattice wording review workflows, especially Chinese/English academic proposal wording shaped by Professor Cheng Yan's revisions. Trigger when the user asks for “措辞 skill”, “Lattice Wording”, “用措辞库审查”, “使用” in the context of wording review, or asks to add new teacher comments/manual wording rules into the wording knowledge base. Supports two modes: supplement/update the wording library, and reverse-review drafts against that library.
---

# Lattice Wording

## Purpose

Use this skill as a child skill of Lattice Research Skill for wording-level academic writing checks. It stores Professor Cheng Yan's wording preferences and applies them back to new drafts.

The canonical library is `references/WORDING_LIBRARY.md`. Read it before reviewing or updating wording rules.

## Mode Selection

Use **Supplement Mode** when the user:

- says a teacher has new edits or comments;
- provides manual wording rules to add;
- asks to update, append, or improve the wording knowledge base;
- provides a revised `.docx`, comments, tracked changes, or before/after wording examples.

Use **Review Mode** when the user:

- says “使用” in the context of wording review;
- asks to use the wording skill/library;
- asks whether a draft has wording problems;
- asks to inspect Stage 2/proposal/manuscript wording using teacher preferences.

If both apply, first update the library from the new evidence, then review the target text.

## Supplement Mode

1. Read `references/WORDING_LIBRARY.md`.
2. Extract only reusable wording rules, not one-off content corrections.
3. Classify each new item as:
   - `explicit replacement`: teacher directly replaced words;
   - `style preference`: teacher's wording implies a preference;
   - `concept warning`: a term requires definition, quantification, or evidence;
   - `caption/reference rule`: figure/table/citation wording issue;
   - `template sentence`: reusable sentence pattern.
4. Preserve original evidence when possible: old wording, revised wording, context, source document/comment.
5. Use `apply_patch` to add or revise entries in `references/WORDING_LIBRARY.md`.
6. In the user response, report what was added and how it should be used next time.

Do not add broad grammar tips unless they are supported by teacher edits or explicitly provided by the user.

## Review Mode

1. Read `references/WORDING_LIBRARY.md`.
2. Read or extract the user's target text. For `.docx`, use the docx skill's extraction workflow; for plain text, inspect directly.
3. Audit the text against the library.
4. Report findings in Chinese using this table shape:

| 位置/原文 | 问题类型 | 为什么有问题 | 建议改法 |
|---|---|---|---|

5. Separate:
   - clear teacher-pattern issues;
   - possible wording risks;
   - content/concept issues that need definition or evidence.
6. Prefer concise, actionable replacements over long explanation.
7. If no issue is found, say so and mention any remaining risk, such as needing teacher confirmation for new terminology.

## Review Priorities

Check in this order:

1. Teacher-specific rules in `WORDING_LIBRARY.md`: repeated emphasis, vague gap wording, misused academic nouns such as `barriers`, `supporting gaps`, `central/main`, terms needing quantification, figure captions, citation punctuation, and over-claiming novelty.
2. The six public academic writing modules in `WORDING_LIBRARY.md`: reader-centered clarity, academic argument wording, scientific paper section wording, literature review and citation language, hedging/certainty/honesty, and teacher-specific override.
3. Content/concept risks that need evidence, definition, quantification, or full-text support.
4. General grammar or style issues only after the above higher-priority checks.

When reporting findings, separate clear teacher-pattern issues from public-guide wording risks and content/concept evidence risks.

## Output Style

Write the final response in Chinese unless the user requests English.

When rewriting English academic sentences, provide polished English replacements. Keep them direct and proposal-appropriate.

Do not over-apply the library mechanically. If the current wording is already clear in context, mark it as acceptable rather than forcing a change.
