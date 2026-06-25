# 检索覆盖审计

输出 `find_papers_outputs/tables/search_coverage_audit.csv`，并在报告中只显示风险摘要。

| 检查项 | 结果 | 风险 | 建议 |
|---|---|---|---|
| 数据库来源分布 | 统计 source_name | 单一数据库偏差 | 增加 OpenAlex/Crossref/Semantic Scholar/领域库 |
| 出版社分布 | 统计 covered_publishers | 出版社偏置 | 增加出版社平台或机构库 |
| 期刊分布 | 统计 covered_journals | 少数期刊偏置 | 扩展关键词和引文链 |
| 年份分布 | 解析 year_range | 年份过窄 | 增加早期经典和最新研究 |
| 原始研究/综述比例 | method_types | 只有综述 | 增加原始研究块 |
| 实验/模拟/理论比例 | method_types | 方法类型缺口 | 专项检索缺失类型 |
| 机制分支覆盖 | mechanism_types | 机制分支遗漏 | 增加机制关键词 |
| 变量分支覆盖 | variable_types | 核心变量遗漏 | 增加变量+观测量块 |
| 全文可得比例 | full_text_availability | 深度扫描不足 | 生成 Request |
| 高优先级全文缺失比例 | find_papers_outputs/request_queue | 核心证据阻断 | 请求用户上传 |
| 是否需要引文扩展 | citation audit | 检索不闭合 | 前后向引用 |
| 是否需要种子文献 | 用户输入 | 领域词不稳定 | 请求种子论文 |
