# Pseudo-gap library

Use this library to downgrade broad, tool-like, or weakly supported gap claims before presenting final research gaps.

| Pseudo-gap | Risk | Required check | Acceptable rewrite |
|---|---|---|---|
| 多种数据耦合 | Does not name variables, scale, or evidence blocker | Which data types are missing, paired, or incomparable? | 数据 A 与 B 因缺少 X 条件/变量不能比较 |
| 统一框架 | Replaces the scientific problem with a framework wish | Which existing model fails, and under what boundary condition? | 现有模型不能处理某明确变量或边界条件 |
| 数据归一化 | Normalization is a method, not a gap | Why exactly are data not normalizable? | 缺少温度/面积/压力等字段导致不可比 |
| 一体化平台 | Engineering wish rather than scientific explanation | What evidence chain would the platform test? | 缺少共享字段 schema 阻断某机制验证 |
| 更多变量联合分析 | No variable priority or mechanism path | Which variables are core and co-controlled? | 变量 X/Y 未同时控制，导致机制无法裁决 |
| 结论不同即争议 | Differences may come from conditions or methods | Are systems, protocols, and scales comparable? | 同等条件下仍出现相反机制判断 |
| 某变量未研究 | The variable may be irrelevant | Is the variable measurable and mechanistically important? | 核心变量未报告，削弱某具体比较 |
| 高引用未提 | Citation count does not define coverage | Did later literature cover the boundary? | Benchmark and later studies both miss X |
| 数据库建设 | Database is infrastructure, not a scientific gap | What hypothesis would the database test? | 数据缺失阻断某机制或阈值验证 |
| 统一指标 | Metric design is not a result | What comparison fails without the metric? | 指标缺失导致某类数据不可比 |
| 数值不同即 gap | Numeric differences may come from units, parameter definitions, methods, or conditions | Are the same parameter, unit, material state, boundary condition, and method being compared? | 同一边界条件下参数 P 的新值可能改变模型结论 Y |
| 单篇新值颠覆全领域 | One report may be an anomaly, method artifact, or special condition | Is the new value high-quality, condition-defined, and relevant to the target model? | 在条件 X 下的新测量值 B 挑战旧范围 A |
| 旧文献被稻草人化为单值 | Prior work may have used a range, not one fixed number | What range did earlier studies actually assume or measure? | 旧研究普遍使用 A-B 范围，新证据报告 C |
| 参数变化不影响结论 | A large numerical change may still be outside model sensitivity | Would substituting the new value change stress, threshold, ranking, mechanism, or prediction? | 参数 P 的更新可能改变模型输出 Y，需要重新建模验证 |

## Real-gap minimum

A surviving gap should satisfy at least one condition:

1. A model or experiment fails under a clear boundary condition.
2. A core variable is missing and prevents mechanism adjudication.
3. A key experimental step is under-reported and blocks comparability.
4. Comparable conditions produce conflicting claims.
5. A specific, measurable mechanism hypothesis can be tested.
6. A prior fixed/default parameter or narrow parameter range is substantially revised by later evidence and this revision may change a model or experimental conclusion.

## Parameter-drift minimum

A parameter assumption drift gap should satisfy all core checks:

1. The old literature assumption is represented honestly as a value or range.
2. The new value/range is at least `2x` different under comparable conditions, or the condition-dependence itself is the scientific issue.
3. Unit, parameter definition, material state, and method differences have been audited.
4. The parameter controls a meaningful model or experimental conclusion.
5. Open-domain Anti-Gap search has not found an already completed re-modeling or re-interpretation under the same boundary condition.

Use `>=2x` as a strong reference signal and `>=10x` as a disruptive/collapse signal. A fold difference alone is not sufficient without the comparability and model-impact checks.

## Downgrade rule

When a candidate gap does not meet the minimum, classify it as:

- `pseudo-gap`: broad wording or tool/platform wish.
- `too broad`: some evidence exists, so the claim must be narrowed.
- `evidence blocker`: the problem is missing parameters, methods, or full text.
- `not yet falsified after open search`: external Anti-Gap search did not find a close refuting study under the recorded sources, terms, and date, but global novelty is still provisional.
