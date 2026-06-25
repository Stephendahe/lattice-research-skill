# Zotero DOI import protocol

Use this protocol after retrieval deduplication and relevance screening, before final Request PDF generation.

## Purpose

DOI import is a Lattice Find Papers responsibility. It gives the user a visible Zotero record of which relevant papers were imported, which already have PDFs, and which still need manual PDF handling. It does not prove that a paper's full text was read.

## Scope

Import only screened records with one of these inclusion decisions:

- `include_core`
- `include_variable`
- `include_method`
- `include_parameter`
- `need_full_text`

Do not batch-import `background_only`, `exclude`, or low-relevance records unless the user explicitly asks.

## Collection naming

Use a parent collection named:

```text
Lattice 母文献库
```

Default date batch:

```text
Lattice 母文献库 / YYYY-MM-DD
```

Project or cross-project batch:

```text
Lattice 母文献库 / YYYY-MM-DD - project_name
```

If the available Zotero connector/helper cannot create collections, import into the selected Zotero target, record the limitation, and report the expected collection name to the user.

## Import order

1. Probe Zotero readiness and write/import capability.
2. Deduplicate import candidates by DOI first, then normalized title and author-year.
3. Search Zotero for existing DOI/title matches.
4. Import missing DOI records through BibTeX/RIS when write capability is available.
5. Re-check imported/existing items for attachment PDF, indexed full text, metadata-only status, and manual action.
6. Write the manifest before generating `request_PDF/doi_list.md`.

## Manifest

Write:

```text
find_papers_outputs/tables/zotero_import_manifest.csv
```

Required columns:

```text
paper_id,title,year,doi,inclusion_decision,zotero_target,import_status,zotero_item_key,pdf_status,manual_action,notes
```

Recommended `import_status` values:

- `already_in_zotero`
- `imported_with_pdf`
- `imported_metadata_only`
- `imported_indexed_text_only`
- `manual_pdf_required`
- `failed_metadata_lookup`
- `no_doi`
- `zotero_unavailable`
- `write_not_available`

Recommended `pdf_status` values:

- `pdf_found`
- `indexed_fulltext_only`
- `metadata_only`
- `supplement_found`
- `manual_download_required`
- `not_checked`

## Request PDF handoff

If Zotero has a readable PDF, do not request the main PDF again. If Zotero has metadata only, indexed text only, missing figures/tables, or missing supplements needed for later data/experiment audit, keep the item in `request_PDF/doi_list.md` or the request queue with the missing parts clearly marked.

Do not expose local absolute attachment paths in the final user-visible report.
