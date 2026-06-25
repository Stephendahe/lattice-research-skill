---
name: lattice-gaps
description: Use when the user asks for Lattice Gaps, 找研究空白, data tree/problem tree analysis, project request_PDF evidence, Zotero-backed PDF/full-text reading, parameter assumption drift/collapse, outdated model parameters, pseudo-gap filtering, anti-gap verification, 反研究空白, or direct verification of a proposed gap.
---

# Lattice Gaps

## Overview

Lattice Gaps consumes evidence prepared by Lattice Find Papers and then performs gap discovery or direct Anti-Gap verification. In discovery mode, it builds a project evidence set from local project files, prior Request PDF folders, Lattice Find Papers manifests, and Zotero PDFs/indexed full text when available. It then turns the evidence set into a data tree, a problem tree, a data-problem relation matrix, parameter-drift audits, pseudo-gap red-flag checks, and evidence-bound candidate gaps. Finally it performs open-domain Anti-Gap verification to refute, narrow, or downgrade each candidate before it reaches the final answer.

This skill is downstream of Lattice Find Papers. Lattice Find Papers retrieves and screens literature, imports screened DOI records into Zotero when available, generates `runs/<run_id>/request_PDF/doi_list.md`, writes `find_papers_outputs/tables/zotero_import_manifest.csv`, and collects user-downloaded PDFs. Lattice Gaps reads those outputs. It does not import DOI records, export batches, create Zotero collections, or manage Zotero libraries.

## Modes

- `discovery mode`: use when the user wants to find gaps from project evidence.
- `verify-only mode`: use when the user already has one or more proposed gaps and asks for Anti-Gap, 反研究空白, falsification, narrowing, or whether the gap is real. Skip data-tree/problem-tree discovery unless needed to understand the proposed gap.

## Input Contract

Default input path:

```text
runs/<run_id>/request_PDF/
```

Use this resolution order:

1. If the user gives a Lattice Research Skill run directory, inspect `<run_dir>/request_PDF/` and the run metadata.
2. If the user gives a folder path, inspect that folder for PDFs, full text, DOI lists, BibTeX/RIS/CSV files, notes, and request-paper outputs.
3. If the user gives only a run id and a likely `runs/` root exists in the workspace, resolve `runs/<run_id>/request_PDF/`.
4. If no explicit folder is given, inspect the current project folder for `request_PDF/`, `request papers`, `requested_papers`, `doi_list.md`, and recent Lattice Find Papers outputs.
5. Read `find_papers_outputs/tables/zotero_import_manifest.csv` when available.
6. Probe Zotero read access after project-folder inspection, then read only matching project items, relevant DOI/title matches, or the user-specified Zotero collection.

Read `doi_list.md` and `zotero_import_manifest.csv` as seed and status files, not as proof. DOI metadata can locate Zotero items or request targets, but it cannot support a full-text claim by itself. If only DOI/metadata exists, send the item back to Lattice Find Papers for Zotero import, Request PDF, or manual full-text handling.

## Evidence Sources And Evidence Levels

- Local project scope: inspect the project folder and prior Request PDF folders first. Treat local PDFs and supplements as the strongest starting evidence.
- Zotero read scope: use the Zotero skill/MCP after local inspection. Run readiness checks first; search only by manifest DOI, title, project terms, user-specified collection, or author-year. Use Zotero attachments and indexed full text only when available and relevant to the project.
- Missing evidence scope: if local files and Zotero do not provide full text, figures/tables, or supplements needed for data/experiment claims, classify the item as an evidence blocker and return it to Lattice Find Papers/Request PDF. Do not perform DOI import inside Lattice Gaps.
- Anti-Gap verification scope: after candidate gaps are generated, or immediately in verify-only mode, search externally enough to challenge each candidate. Use academic search, publisher pages, review papers, citation chains, adjacent terminology, preprints, databases, benchmarks, standards, and method/protocol literature when available.
- Final claim scope: do not claim a gap is globally proven absent. State the searched sources, terms, date, and remaining uncertainty.

Evidence levels:

- `L0_metadata`: DOI, title, bibliographic record, citation metadata.
- `L1_abstract`: abstract, snippet, indexing page, or secondary summary.
- `L2_indexed_text`: Zotero indexed full text, HTML text, or partial readable text without figures/tables.
- `L3_full_text`: readable PDF/full text with methods, results, figures, and tables.
- `L4_supplement`: supplementary methods, tables, raw parameter files, datasets, or code.

Parameter values and model assumptions should be treated as strong evidence only at `L3_full_text` or higher unless the value is explicitly visible in an authoritative online table, dataset, standard, or preprint full text.

## Hard Boundaries

- Do not skip project-folder inspection before going to Zotero or online search.
- Do not scan a whole Zotero library without project constraints; searches must be bounded by DOI list, title, project name, material/system, mechanism, parameter, or author-year.
- Do not write to Zotero, import DOI records, export batches, or create collections. Those actions belong to Lattice Find Papers.
- Do not use abstracts as full-text evidence.
- Do not treat online metadata-only fallback as a data/experiment gap proof. It can refute, narrow, or locate evidence during Anti-Gap verification, but it cannot replace full text, figures/tables, supplements, datasets, or methods.
- Do not produce detailed per-paper literature annotations; use only compact evidence anchors such as filename, page, figure, table, or section.
- Do not treat "unified framework", "multi-factor coupling", "data normalization", "database/platform", or "more variables" as a gap unless it survives open-domain Anti-Gap verification.
- Do not treat a numeric difference as a parameter gap until unit, parameter definition, material state, boundary condition, and measurement/modeling method have been checked.

## Workflow

1. Build the project evidence set.
   - Inspect the project folder and prior request-paper folders first.
   - List PDFs, supplements, full-text files, `doi_list.md`, `zotero_import_manifest.csv`, BibTeX/RIS/CSV files, and Lattice Find Papers outputs.
   - Extract DOI/title/author-year seeds and mark which items have local full text, Zotero PDF, indexed full text, metadata only, or manual-download status.
   - Separate primary papers from secondary/background papers using the user's topic, filenames, DOI list, and available metadata.

2. Probe Zotero and read matching evidence.
   - Use the Zotero skill/MCP readiness check before Zotero operations.
   - Determine whether Zotero is readable.
   - Search Zotero by DOI/title/project terms and record whether each match has attachment PDF, indexed full text, metadata only, or no match.
   - Use metadata-only or indexed-full-text-only items as evidence-level markers, not as full-text proof.

3. Decide mode.
   - If the user provides proposed gaps and asks for verification, switch to `verify-only mode` and jump to step 10.
   - If the user asks for discovery, continue through the full evidence analysis.
   - If evidence is insufficient for discovery, output the missing PDFs/supplements/datasets and route back to Lattice Find Papers or Request PDF.

4. Scan sources by role and evidence level.
   - Primary papers: read Results, Figures/Tables, Methods/SI, Discussion, and limitations.
   - Secondary papers: use only for context, method comparison, or boundary conditions.
   - Zotero indexed full text: use as partial text only; do not infer figure/table data unless the attached PDF or table is readable.
   - Online metadata/abstracts: use only for Anti-Gap refutation, narrowing, or locating items that should return to Lattice Find Papers/Request PDF; do not use them for full-text conclusions.
   - Record evidence anchors, not long quotations.

5. Build the data tree.
   - Start from observed objects and data families.
   - For defect-focused topics, organize by defect type, size, depth, length, shape, density, distribution, measurement method, scale, condition, and outcome.
   - For parameter-focused topics, organize by parameter name, value/range, unit, material/system, state variable, boundary condition, measurement/model method, year, and evidence level.
   - Keep variable names measurable and comparable.

6. Build the problem tree.
   - Split the topic into scientific questions such as starting point, propagation, energy, boundary condition, scale transfer, mechanism, and method visibility.
   - Convert broad topics into testable questions.

7. Build the data-problem relation matrix.
   - Link data nodes to problem nodes using relation types: supports, contradicts, correlates_with, causes_claimed, modulates, measures, not_reported, incomparable, and only_tested_under.
   - Mark whether each relation is direct evidence, inference, missing evidence, or blocker.

8. Identify candidate gaps inside the evidence set.
   - Missing node: a core variable or mechanism is absent from all readable evidence sources.
   - Weak edge: a relation is claimed but not measured.
   - Contradiction: comparable conditions lead to conflicting claims.
   - Boundary gap: evidence exists only under narrow materials, scales, or test conditions.
   - Method gap: current methods cannot observe the claimed process.
   - Reporting blocker: missing parameters make comparison impossible.
   - Parameter assumption drift: earlier work uses a fixed/default parameter or narrow range, while later evidence reports a substantially different or state-dependent value that could change model or experimental conclusions.

9. Run the parameter assumption drift audit and pseudo-gap red-flag filter when parameter values matter.
   - Extract old values as ranges when the literature uses ranges, not as a strawman single value. Example: treat Li modulus as 30-50 MPa if that is the practical range, not only 50 MPa.
   - Normalize units and parameter definitions; distinguish Young's modulus, shear modulus, storage modulus, hardness, fitted effective modulus, and model calibration parameters.
   - Compare material state and boundary conditions: volume/SOC, temperature, pressure, strain rate, phase, microstructure, loading path, interface condition, and measurement/model method.
   - Flag `>=2x` inconsistency as a strong reference signal when conditions are comparable or the condition-dependence itself is the scientific issue.
   - Flag `>=10x` inconsistency, new state-dependence, or direction-changing thresholds as disruptive/collapse signals.
   - Ask whether replacing the old parameter range with the new value would change stress, strain, failure threshold, interface stability, crack initiation, dendrite growth, or another model conclusion.
   - Compare wording with `references/PSEUDO_GAP_LIBRARY.md`; pseudo-gap detection is a red-flag filter, not the final judgment.
   - If a text file is provided, optionally run `scripts/detect_pseudo_gaps.py` to catch common pseudo-gap phrases before manual evidence review.
   - Rewrite any surviving gap as: "Under boundary condition X, prior models/experiments assumed parameter P in range A, while later evidence reports P as B or state-dependent; it remains untested whether updating P changes conclusion Y."

10. Apply embedded Anti-Gap verification.
   - Read `references/PSEUDO_GAP_LIBRARY.md`.
   - Restate each candidate/proposed gap narrowly. Do not broaden it.
   - Build searches from mechanism terms, variable names, material/system names, boundary conditions, methods, synonyms, abbreviations, adjacent-field terminology, and likely review/benchmark terms.
   - For parameter drift, search old parameter names/ranges, new reported values, state variables, model sensitivity terms, "revisited", "updated parameter", "finite element", "calibration", "benchmark", and the specific material/interface.
   - Search outside the initial evidence set to find prior studies, datasets, validated methods, negative results, reviews, benchmarks, standards, protocols, or preprints that could refute the candidate.
   - Record searched sources, exact terms, and search date.
   - Classify as `survives narrowly`, `too broad`, `pseudo-gap`, `evidence blocker`, `not yet falsified after open search`, or `refuted by external evidence`.
   - Rewrite surviving gaps as mechanism-variable-boundary-condition claims.

## Verify-Only Mode

Use this mode when the user already has proposed gaps.

1. Restate the proposed gap exactly in one sentence.
2. Identify what would refute it: same mechanism, parameter, dataset, method, material system, boundary condition, or completed re-modeling/re-interpretation.
3. Check `references/PSEUDO_GAP_LIBRARY.md` for red flags.
4. If a text file is provided, optionally run `scripts/detect_pseudo_gaps.py` before manual review.
5. Inspect any provided local PDFs/Zotero evidence if available.
6. Run only the external checks needed to falsify or narrow the proposed gap.
7. Return a judgment: `refuted`, `too broad`, `pseudo-gap`, `evidence blocker`, `not yet falsified after open search`, or `survives narrowly`.

Do not invent new gaps in verify-only mode unless the user explicitly asks for new gap discovery.

## Output Format

Respond in Chinese by default.

Use these sections:

1. `模式`: discovery mode or verify-only mode.
2. `证据集合边界`: project path, request folders inspected, Zotero read status, readable PDFs/full texts, manifest status, and what the evidence set can/cannot prove.
3. `文献主次分组`: primary vs secondary papers, with one-line roles and evidence level.
4. `Zotero 读取记录`: Zotero read status, matched item status, indexed-full-text-only items, metadata-only items, and blockers. Do not report import/export actions.
5. `数据树`: hierarchical bullet tree of data/variables.
6. `问题树`: concise scientific questions; keep brief when parameter/experiment tables carry the main result.
7. `数据-问题关系矩阵`: compact table linking data nodes, problem nodes, relation type, evidence state, and anchor.
8. `参数假设漂移审计`: table with parameter, old range/default, new value/range, fold difference, conditions, evidence level, likely model impact, and judgment.
9. `伪 gap 红旗`: pseudo-gap red flags from the library and whether each was cleared, downgraded, or still unresolved.
10. `开放反验证范围`: searched sources, exact terms, date, and known blind spots.
11. `候选 gap 反验证`: Anti-Gap table with candidate/proposed gap, falsification question, risky evidence, external search result, judgment, and rewrite.
12. `可暂时保留的研究空白`: only gaps that survive narrowly after open-domain verification.
13. `被降级的问题`: pseudo-gaps, too-broad claims, refuted claims, and evidence blockers.
14. `下一步最小验证`: the smallest additional PDF, search branch, Lattice Find Papers rerun, experiment, data extraction, sensitivity analysis, or manual Zotero/PDF action needed to challenge the surviving gaps.
