# 多源检索协议

Lattice Find Papers 不能依赖单一数据库。每个主题至少拆成多个检索块，并尽量跨 OpenAlex、Crossref、Semantic Scholar、Google Scholar 或等价学术搜索、PubMed/IEEE/ACM/arXiv/ChemRxiv/bioRxiv/CORE、出版社平台、用户种子文献、后向引用、前向引用和相似文献。

| 检索块 | 查询组合 | 目的 |
|---|---|---|
| 对象 + 现象 | research object + phenomenon | 找核心文献 |
| 对象 + 机制 | research object + mechanism | 找机制解释 |
| 变量 + 观测量 | variable + observable | 找变量关系 |
| 变量 + 方法 | variable + method | 找变量控制 |
| 机制 + 争议 | mechanism + contradiction / discrepancy | 找冲突 |
| 参数 + 模型 | parameter + model | 找参数 |
| 流程 + 可重复性 | procedure + reproducibility | 找实验漏洞 |
| 种子文献 + 引用 | seed + citations | 找经典与后续 |

必须记录检索日期、检索式、来源、返回数量、去重后数量、覆盖的出版社/期刊/年份/方法/机制/变量。每个来源初始可取 100-500 条，去重后候选池通常 300-3000 条；用户指定范围优先。连续两轮扩展新增核心文献低于 5% 时，可建议停止。

如果当前环境不能检索网络，不要假装检索完成。输出多源检索计划、建议检索式和人工检索清单，等待用户提供文献、导出文件或可用检索工具后继续。
