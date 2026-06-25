# Request 文献目录协议

Request 文献目录不是失败输出，而是合格的诚实输出。它说明当前证据边界在哪里，以及下一步需要什么材料。

生成 Request 文献目录前，必须先完成筛选后 DOI 的 Zotero 导入/匹配、全文可得性检查，并更新 `zotero_import_manifest.csv` 与 `full_text_availability.csv`。检查包括 Zotero Local API、Zotero 导出文件、在线开放全文、本地 PDF 文件夹、本地补充材料文件夹和用户手动文件路径清单；这些只是全文可得性检查的子步骤。

生成条件：重要文献在在线和本地检查后仍只有 L0/L1；缺 Methods/Results/Figures/Tables/Supplementary；文献可能支撑核心机制、关键数据、机制冲突、benchmark、关键变量或实验流程细节。

字段：request_id、paper_id、title、year、doi、source_url、current_access_level、why_full_text_needed、needed_sections、missing_for_tasks、priority、user_action、resume_checkpoint、notes、zotero_import_status、zotero_item_key、local_library_checked、local_library_result、local_resolution_status。

同时生成 `runs/<run_id>/request_PDF/doi_list.md`。`request_PDF/` 是用户下载 PDF 的固定文件夹，也是 Lattice Gaps 的默认全文输入文件夹。用户根据 `doi_list.md` 下载 PDF 后，把 PDF 直接放在同一个 `request_PDF/` 中；不要另建 handoff、find_a_gap_pdfs 或其他临时目录。

`doi_list.md` 必须只包含两个列表：

```markdown
## DOI

- 10.xxxx/example

## Web Links

- Title: Example title
  Authors: Zhang et al.
  Year: 2024
  Link: https://doi.org/10.xxxx/example
```

DOI 列表只写 DOI 值，不写标题或解释。Web Links 列表写 title、authors、year、link；link 优先用 `source_url`，没有可用官网链接时用 `https://doi.org/<doi>`。缺 DOI 的文献不进入 DOI 列表，但如果有可用链接，仍可进入 Web Links。

Request 规则：如果本地找到主文 PDF，则不再 Request 主文；如果本地找到主文 PDF 但缺补充材料，且实验轮需要补充材料，则只 Request 补充材料；如果只找到 Zotero 条目，没有 PDF，仍然 Request 全文；如果只找到 indexed full-text，没有 PDF，仍然 Request PDF，除非用户只要求正文级初筛；低置信度本地匹配不得自动移出 Request，只标记为需要人工确认；本地找到 PDF 后，后续流程从全文分轮扫描继续。

Lattice Gaps 对接规则：`request_PDF/` 仍是 Lattice Find Papers 到 Lattice Gaps 的主要本地交接目录。Lattice Gaps 还可以读取 Lattice Find Papers 生成的 `zotero_import_manifest.csv` 和相应 Zotero 条目/附件，但不再执行 DOI 导入、批量导出或 Zotero collection 管理。如果 Lattice Gaps 发现只有 DOI 或 metadata、缺全文/图表/补充材料，应要求回到 Lattice Find Papers 执行 Zotero 导入、Request PDF 或手动补全文献。Lattice Gaps 的 Anti-Gap 反验证阶段可以进行开放域检索来推翻或缩窄候选 gap，但在线兜底不得被写成全文级数据或实验结论。

priority 规则：high 表示核心机制/关键数据/冲突/benchmark/关键变量；medium 表示相关但非主线；low 表示背景或引文追踪。当前只能基于摘要判断时，不得把该文献用于数据关系强结论、实验流程漏洞结论或机制冲突裁决。
