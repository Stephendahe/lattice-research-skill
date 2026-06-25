# 全文可得性协议

每篇候选文献必须写入 `find_papers_outputs/tables/full_text_availability.csv`。全文可得性检查应接在 DOI 导入 Zotero 之后执行：先检查 Zotero 中已导入/已存在条目的 PDF、indexed full text 和 metadata-only 状态，再检查在线开放全文、本地 PDF 文件夹、本地补充材料文件夹和用户手动路径清单，最后更新全文状态。不要把本地检查扩展成独立大模块。

| 状态 | 含义 |
|---|---|
| metadata_only | 只有元数据 |
| abstract_only | 只有标题摘要 |
| partial_text | 有部分正文 |
| full_text_available | 有全文 |
| figures_available | 有图表 |
| supplement_available | 有补充材料 |
| supplement_missing | 缺补充材料 |
| paywalled_or_unavailable | 当前无法访问 |
| user_uploaded | 用户已上传 |
| needs_user_upload | 需要用户上传 |

## 本地全文检查

只对以下文献执行 Zotero 和本地检查：已通过标题摘要初筛；`inclusion_decision` 为 include_core、include_variable、include_method、include_parameter 或 need_full_text；后续数据轮、实验轮、机制轮或可比性轮需要全文支持。不要对 background_only、exclude 或低相关文献扫描 Zotero，除非用户明确要求。

生成 Request 前按顺序检查：Zotero Local API（默认 `http://localhost:23119/api/`）和 DOI 导入 manifest、Zotero 导出的 BibTeX / Better BibTeX / CSL JSON / RIS、在线开放全文、用户指定本地 PDF 文件夹、用户指定补充材料文件夹、用户手动文件路径清单。Zotero 不可访问只写一条 warning，不中断流程；不要反复要求配置 Zotero；不要直接读取 `zotero.sqlite`；不要绕过权限；不要上传或外传本地 PDF；最终报告不得暴露本地绝对路径。

本地匹配优先级：DOI 精确匹配；Zotero citation key 匹配；标题规范化精确匹配；第一作者 + 年份 + 期刊匹配；标题模糊匹配。只有 high 或 medium confidence 可以自动更新全文状态；low 或 tentative 只能标记为需要人工确认，不得自动视为已有全文。

本地全文状态包括：not_found、metadata_only、abstract_only、indexed_fulltext_only、pdf_found、html_found、supplement_found、raw_data_found、code_found、needs_manual_confirmation。只找到 Zotero 条目仍为 L0；只有摘要仍为 L1；只有 indexed full-text 标记为 L2_partial_text，不得进入图表/数据深度分析；找到主文 PDF 可标记 L2_full_text；找到可读图表/表格可标记 L3_figures_tables；找到补充材料可标记 L4_supplementary；找到原始数据或代码可标记 L5_raw_data_code。

只有摘要时不能做数据轮；没有 Methods 时不能做实验轮；没有 Figures/Tables 时不能做图表数据抽取；没有 Supplementary 时不能做完整实验流程审计。不得绕过付费墙，不得假装读过无法访问的全文。缺少关键部分时，进入 Request 文献目录。
