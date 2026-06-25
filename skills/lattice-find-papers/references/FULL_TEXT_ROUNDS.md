# 全文分轮专项扫描

| 轮次 | 扫描章节 | 抽取字段 | 不允许做的事 | 输出表格 | 证据等级 |
|---|---|---|---|---|---|
| 结构轮 | 标题、摘要、章节、图表标题、SI 目录 | Methods/Results/Discussion/Figures/Tables/SI 位置 | 不做实质结论 | evidence_spans | L2-L4 |
| 数据轮 | Results、Figures、Tables、Supplementary Data | 变量、观测量、数值、单位、趋势、误差、统计 | 不从摘要提取定量关系 | variable_relations、evidence_spans | L2-L4 |
| 实验轮 | Methods、Experimental、Supplementary Methods | 材料来源、前处理、制备、组装、测试协议、控制/未控制变量 | 不把未报告写成已控制 | experiment_pipeline_audit | L2/L4 |
| 机制轮 | Results、Discussion、Conclusion | 机制链、作者解释、替代解释、边界条件、限制 | 不用 Discussion 替代数据证据 | mechanism_comparison | L2-L4 |
| 可比性轮 | Methods + Results + Figures + SI | 体系、流程、尺度、单位、数据处理差异 | 不强行归一化 | normalization_blockers | L2-L4 |
| 矛盾轮 | 跨文献对应字段 | 真冲突/条件差异/变量控制差异/尺度差异 | 不基于摘要裁决冲突 | mechanism_conflicts | L2-L4 |
| 引用扩展轮 | Introduction、Related Work、References | 经典来源、原始证据、遗漏关键词、引文链 | 不把综述当原始数据 | citation_audit、retrieval log | L0-L2 |
