# Wording Library

来源：Professor Cheng Yan 对 `Stage2_Xuanhe_draft_v1 after CY.docx` 的 tracked changes 与 comments，以及 Stephen 后续人工补充的规则。

用途：审查 Stage 2 proposal、research plan、manuscript draft、progress report 中的措辞风险。新增老师意见时，继续往本库补充。

## 1. Explicit Replacements

| 原写法 | 推荐写法 | 规则 | 可复用模板 |
|---|---|---|---|
| `Barriers in phase-field modelling` | `Limits in phase-field modelling` / `Limitations of phase-field modelling` | 写方法局限时，`limits/limitations` 更学术、更中性；`barriers` 更像外部障碍、政策壁垒或不可逾越障碍。 | `Limitations of the phase-field model include parameter uncertainty, simplified chemistry and numerical stiffness.` |
| `points to one central gap` | `indicates there is a main gap` | `points to` 偏口语/比喻；proposal 中优先用 `indicates`, `shows`, `identifies`, `suggests`。 | `The preliminary review indicates that there is one main gap and two associated gaps.` |
| `central gap` | `main gap` | 不要堆叠强调词；`main central gap` 冗余。教授这次更偏好简单的 `main gap`。 | `The main gap is the lack of a benchmarked LLZTO-centred instability criterion.` |
| `supporting gaps` | `associated gaps` | `gap` 不太会 support 另一个 gap；用 `associated`, `secondary`, `related`, `narrower` 更自然。 | `Two associated gaps are parameter uncertainty and benchmarking inconsistency.` |
| `main central gap` | `main gap` | `main` 与 `central` 语义重复，保留一个即可。 | `The main gap is...` |

## 2. Style Preferences

| 风险写法 | 推荐策略 | 原因 | 示例 |
|---|---|---|---|
| `key/main/central/important` 多个形容词连续堆叠 | 只保留一个最准确的限定词 | 学术写作要精准，不靠形容词堆强度。 | `The main gap is...` |
| 抽象地说 `this project addresses barriers` | 说清楚是 `addresses limitations` 或 `manages uncertainty` | `barrier` 暗示障碍本身，`limitation` 更适合方法边界。 | `The project addresses these limitations through bounded parameters and explicit benchmarking.` |
| 用 `points to` 引出文献结论 | 用 `indicates`, `suggests`, `shows`, `identifies` | 更正式、更直接。 | `The preliminary review indicates...` |

## 3. Concept Warnings

这些词不是绝对不能用，但一旦出现，就要补定义、参数、测量方法或验证路径。

| 高风险词 | 老师关注点 | 写作要求 | 推荐表达 |
|---|---|---|---|
| `defects` | How do we quantify these defects? What is the size scale, micro or nanosized? | 不要只写 defects；说明 size scale、density、morphology、measurement method。 | `Defects will be quantified by SEM/FIB-SEM in terms of size, density, aspect ratio and position relative to grain boundaries.` |
| `electrochemical weakening` | What is this electrochemical weakening? Provide more information. | 明确 weakening 是 reduction/corrosion/electronic leakage 导致 fracture energy、modulus 或 cohesive strength 下降。 | `Electrochemical weakening refers here to local reduction or corrosion that lowers effective fracture resistance, represented phenomenologically as a charge- or overpotential-dependent reduction in Gc.` |
| `dominated parameter` | Need to understand the dominated parameter controlling dendrite growth. | 应写 `dominant parameter` 或 `dominant controlling parameter`。 | `The first sensitivity study will identify the dominant controlling parameters, including current density, surface roughness, stack pressure and defect size.` |
| `nanoscale Li strength` | Can be evaluated using in situ SEM nanoindentation. | 提到 Li/LLZTO mechanics 时，要联系 size-dependent properties 和实验/文献来源。 | `Size-dependent Li mechanical properties will be constrained using literature data and, where feasible, in situ SEM nanoindentation of Li features.` |
| `phase-field simulation` | Add details: basic equations and materials constitutive laws. | 不能只说 develop a phase-field model；要给变量、方程、本构和边界条件。 | `The model will couple Li transport, Butler-Volmer plating kinetics, mechanical equilibrium and phase-field fracture through the fields c, phi, d and u.` |
| `innovation` / `novelty` | What is the innovation of your research? These problems have been investigated by others. | 不要泛泛说 novel；要写“与已有 phase-field modelling 的差异”。 | `The innovation is not phase-field modelling itself, but an LLZTO-specific, parameter-bounded mechanism map constrained by measured defect geometry and size-dependent mechanical properties.` |

## 4. Caption and Citation Rules

教授多次删除图注中的长版权说明，例如：

- `Reproduced from ... DOI ... under CC BY...`
- `Adapted from ... publisher permission required...`
- `source licence CC BY-NC-ND... formal permission should be checked...`

### Rule

图注应服务阅读，只保留图展示什么和引用。版权、licence、permission 信息不要塞进 caption，除非模板明确要求。

### Avoid

`Figure 3. Li plating-induced cracking in LLZTO. Adapted from Porz et al. (2017), DOI: ..., publisher permission required for reuse beyond proposal discussion. [12]`

### Prefer

`Figure 3. Li plating-induced cracking in LLZTO. [12]`

若需要版权记录，单独建 `Figure permissions` 表，放在附录或内部材料里。

### Punctuation

Caption 末尾保持一个句点。避免 `.. [9]`、`[9]. .` 或删除/插入来源说明后残留多余标点。

Preferred formats:

- `Figure 2. Local Li-flux, stress build-up and fracture sequence in LLZTO. [9]`
- `Figure 2. Local Li-flux, stress build-up and fracture sequence in LLZTO [9].`

全文选一种格式保持一致。

## 5. Self-Check Before Sending to Professor

1. 有没有把 `barriers` 用在方法局限上？若有，优先改成 `limits` 或 `limitations`。
2. 有没有 `main central`, `key central`, `major main` 这类重复强调？删掉一个。
3. 有没有 `supporting gap`？优先改成 `associated gap`, `secondary gap`, `related gap`。
4. 有没有 `points to`？正式 proposal 里优先改成 `indicates`, `shows`, `identifies`, `suggests`。
5. 有没有只写 `defects`、`weakening`、`phase-field model`，但没有定义、参数或测量方法？必须补一小句。
6. 图注是不是太长？图注只保留“图展示什么 + 引用”，版权信息另放。
7. 每个 figure caption 结尾是否只有一个句点，引用格式是否统一？
8. 有没有声称 innovation 但没有说清楚和已有 phase-field work 的区别？

## 6. Reusable Sentences

`The preliminary review indicates that there is one main gap and two associated gaps.`

`The main gap is the lack of a benchmarked, LLZTO-centred instability criterion.`

`Two associated gaps are parameter uncertainty and benchmarking inconsistency.`

`The limitations of the phase-field model include parameter uncertainty, numerical stiffness and simplified chemistry.`

`Defects will be quantified by SEM/FIB-SEM in terms of size, density, aspect ratio and position relative to grain boundaries.`

`Electrochemical weakening refers to local reduction or corrosion that lowers effective fracture resistance under electrochemical driving force.`

`The sensitivity analysis will identify the dominant controlling parameters for Li penetration.`

`The innovation is not phase-field modelling itself, but an LLZTO-specific, parameter-bounded mechanism map constrained by measured defect geometry and size-dependent mechanical properties.`

## 7. Public Academic Writing Modules

这些模块来自公开、可信的大学写作中心、教授写作指南、期刊/出版社训练材料和学术短语资源。它们用于补充老师个人偏好，但不覆盖老师明确修改过的规则。使用时优先级为：

1. 老师明确修改或评论；
2. Stephen 针对自己课题补充的规则；
3. 本节公开资料模块；
4. 通用语法和风格判断。

不要把公开资料中的短语整段复制进文章。Lattice Wording 应把它们转化为审查规则、风险提示、改写策略和少量原创模板。

### Source Register

| source_id | 来源 | 主要用途 |
|---|---|---|
| `harvard_writing_guides` | Harvard Writing Project / Harvard College Writing Center writing guides | thesis、paragraph、transition、counterargument、style and conventions |
| `pinker_classic_style` | Steven Pinker, Harvard, writing on academic style and clarity | reader-centered clarity, curse of knowledge, classical style |
| `gopen_swan_scientific_writing` | George Gopen and Judith Swan, "The Science of Scientific Writing" | reader expectations, topic position, stress position, information flow |
| `oxford_scientific_writing` | Oxford MPLS scientific writing resources | clear sentences, active voice when appropriate, smothered verbs, acronym discipline |
| `cambridge_style_plain_english` | University of Cambridge style guide and writing resources | one idea per sentence, plain English, short words where possible |
| `mit_scientific_paper` | MIT OCW scientific paper writing guidance | section-specific research paper wording |
| `manchester_phrasebank` | University of Manchester Academic Phrasebank | rhetorical functions, literature review language, cautious phrasing |
| `oxford_opal` | Oxford Phrasal Academic Lexicon written phrases | academic phrase functions and vocabulary families |
| `newcastle_reporting_verbs` | Newcastle University Academic Skills Kit, reporting verbs | citation stance and reporting verb categories |
| `bloch_reporting_verbs` | Bloch 2010, Journal of Writing Research, reporting verbs study | corpus-informed reporting verb use and stance |
| `nature_readability` | Nature Masterclasses writing for readability/impact | active voice and readability in scientific writing |
| `pnas_first_person` | PNAS article on first-person voice in scientific writing | first-person and active voice as readability tools |

### Module 1. Reader-Centered Clarity

Sources: `pinker_classic_style`, `gopen_swan_scientific_writing`, `cambridge_style_plain_english`, `harvard_writing_guides`.

| rule_id | 检查点 | 风险信号 | 改写策略 | 可复用模板 |
|---|---|---|---|---|
| `clarity_reader_first` | 读者是否能在第一遍读懂主语、动作和结论 | 长句先堆背景、最后才出现主张 | 先写核心主张，再补限定条件 | `This section argues that [claim], under [condition].` |
| `clarity_topic_stress` | 句子开头是否承接旧信息，句末是否放重要新信息 | 重要发现埋在句中；句末落在弱词上 | 让已知对象在前，关键结果/差异/限制在句末 | `Previous models treat [old information]; this project tests [new contribution].` |
| `clarity_one_idea` | 一句话是否只承担一个核心 idea | 一个句子同时解释背景、方法、结果、意义 | 拆成两句或三句；每句只推进一步 | `The model first defines [X]. It then tests [Y].` |
| `clarity_subject_verb` | 主语和主要动词是否距离过远 | 主语后插入多层从句，读者找不到动作 | 把主语和动作靠近；把条件移到句首或句末 | `The simulation compares [A] with [B] under [condition].` |
| `clarity_plain_terms` | 是否用复杂词替代了更清楚的普通词 | `utilise`, `facilitate the implementation of`, `in order to` | 用短词，但不牺牲专业精度 | `use`, `enable`, `to` |

### Module 2. Academic Argument Wording

Sources: `harvard_writing_guides`, `oxford_scientific_writing`, Oxford essay/dissertation guidance, Cambridge HPS writing advice.

| rule_id | 检查点 | 风险信号 | 改写策略 | 可复用模板 |
|---|---|---|---|---|
| `argument_answer_question` | 段落是否在回答具体问题，而不是堆知识 | 段落只介绍背景，没有判断 | 先写本段回答什么问题 | `This paragraph evaluates whether [factor] can explain [phenomenon].` |
| `argument_claim_evidence_link` | claim 后是否马上给 evidence 或验证路径 | `This is important` 后没有原因 | 用 because / by / through 连接依据 | `[Claim] because [evidence or mechanism].` |
| `argument_gap_specificity` | gap 是否具体到机制、变量、边界或证据缺口 | `lack of a unified framework`, `few studies considered multiple factors` | 改成具体 blocker 或 testable opportunity | `The unresolved issue is whether [specific variable] changes [specific mechanism] under [condition].` |
| `argument_transition_function` | 转折词是否表达真实逻辑关系 | `However` 只是换话题 | 标明 contrast、extension、cause、limitation | `However, this evidence does not establish [missing causal link].` |
| `argument_counter_scope` | 反驳是否被准确限定 | 把所有 prior work 写成 insufficient | 说明 prior work 做到了什么、没做到什么 | `Although [study] establishes [A], it does not test [B].` |

### Module 3. Scientific Paper Section Wording

Sources: `mit_scientific_paper`, `oxford_scientific_writing`, `nature_readability`, `pnas_first_person`, Elsevier Researcher Academy writing resources.

| section | 该部分要完成什么 | 常见措辞风险 | 改写策略 | 可复用模板 |
|---|---|---|---|---|
| `Title` | 准确呈现对象、机制和贡献 | 过宽、像口号、没有对象 | 放入 material / method / mechanism / outcome | `[Mechanism] of [phenomenon] in [material/system] under [condition]` |
| `Abstract` | 用少量句子交代问题、方法、结果、意义 | 只列 equipment 或 technique，没有核心结果 | 每句服务一个功能：problem, method, result, implication | `We show that [main result], suggesting [bounded implication].` |
| `Introduction` | 从领域问题收束到本研究问题 | 背景过长，gap 太抽象 | 最后一段明确 gap、objective、approach | `Here, we test whether [specific gap] by [approach].` |
| `Methods` | 让实验/模型可复核 | 用 vague verbs：`study`, `explore`, `consider` | 写清材料、参数、边界条件、算法或测量方法 | `[Parameter] was varied from [range] while [control] was held constant.` |
| `Results` | 报告观察和数据，不提前过度解释 | Results 里写 speculative mechanism | 先描述结果，再把解释留到 Discussion | `[Observable] increased from [A] to [B] when [condition changed].` |
| `Discussion` | 解释结果、边界和替代解释 | 过度外推，直接写 proves | 区分 supports, suggests, is consistent with, does not rule out | `These results are consistent with [mechanism], but do not rule out [alternative].` |
| `Figure caption` | 说明图展示什么和关键变量 | 图注太长、版权信息塞入 caption | 保留图意 + 变量 + 引用；版权另记 | `Figure X. [Observable] as a function of [variable] in [system]. [ref]` |

Voice rule: 主动语态和第一人称可以提高可读性，但不是机械要求。Methods 中需要突出过程或对象时可用被动语态；需要突出作者动作、逻辑选择或贡献时优先主动语态。

### Module 4. Literature Review And Citation Language

Sources: `manchester_phrasebank`, `oxford_opal`, `newcastle_reporting_verbs`, `bloch_reporting_verbs`.

| rule_id | 检查点 | 风险信号 | 改写策略 | 可复用模板 |
|---|---|---|---|---|
| `citation_verb_stance` | reporting verb 是否表达正确立场 | 所有文献都用 `says`, `shows`, `proves` | 按功能选择 verb：reports / suggests / argues / demonstrates / questions | `[Author] reports that [finding].` |
| `citation_neutral_vs_evaluative` | 是否区分中性描述和批判评价 | 引文动词偷偷改变原文强度 | 只在有证据时用 evaluative verb | `[Author] suggests [claim], but the study does not measure [missing variable].` |
| `citation_integrated_argument` | 文献是否服务自己的论证 | 一段一个 citation list，没有 synthesis | 每组文献后加 synthesis sentence | `Together, these studies indicate [pattern], but leave [blocker] unresolved.` |
| `citation_tense_choice` | 引文时态是否稳定 | present/past/present perfect 混乱 | 领域常识用 present；具体研究结果可用 past；研究趋势用 present perfect | `Recent studies have examined [topic], but few have quantified [variable].` |
| `citation_gap_not_attack` | 批评 prior work 是否公正 | `Previous studies failed to...` 过强 | 写成 scope limitation，而不是贬低 | `Previous studies focused on [A], leaving [B] less well constrained.` |

Reporting verb families:

- Neutral: `reports`, `describes`, `observes`, `outlines`, `examines`.
- Tentative/result-oriented: `suggests`, `indicates`, `is consistent with`, `points to`（正式 proposal 中慎用）.
- Strong evidence: `demonstrates`, `establishes`, `shows`（只在证据足够时使用）.
- Argument/interpretation: `argues`, `proposes`, `interprets`, `attributes`.
- Critical/limiting: `questions`, `challenges`, `does not account for`, `does not distinguish`.

### Module 5. Hedging, Certainty And Honesty

Sources: `manchester_phrasebank`, `oxford_opal`, `pnas_first_person`, Lattice Honesty.

| rule_id | 检查点 | 风险信号 | 改写策略 | 可复用模板 |
|---|---|---|---|---|
| `hedge_strength_match` | 结论强度是否匹配证据强度 | 摘要级证据写成 `proves` / `demonstrates` | 按证据等级降级动词 | `The evidence suggests that [claim], but full-text verification is needed.` |
| `hedge_avoid_overhedging` | 是否过度谨慎导致没有贡献 | 连续使用 `may`, `might`, `possibly`, `seems` | 保留一个限定词，并明确证据基础 | `These data support [bounded claim] under [condition].` |
| `hedge_scope_boundary` | 是否写出适用范围 | 结论没有材料、尺度、条件边界 | 加 material / condition / method boundary | `Within the tested [range/system], [result] indicates [claim].` |
| `hedge_correlation_causation` | 是否把相关写成因果 | `leads to`, `causes`, `drives` 无机制证据 | 改为 association 或 consistency | `[A] is associated with [B] and is consistent with [mechanism].` |
| `hedge_missing_evidence` | 是否诚实标注缺全文/缺图表/缺 SI | 缺全文仍写机制裁决 | 明确阻断项和下一步 | `This claim requires full-text methods and figure-level evidence before it can be used as a mechanism conclusion.` |

Certainty ladder:

1. `may be associated with` / `is consistent with`：弱证据、摘要级、相关性；
2. `suggests` / `indicates`：有数据但仍有替代解释；
3. `supports`：有明确证据链；
4. `demonstrates` / `establishes`：直接证据强、变量控制清楚；
5. `proves`：科研写作中通常避免，除非是数学/逻辑证明语境。

### Module 6. Teacher-Specific Override Layer

Sources: Professor Cheng Yan tracked changes/comments, Stephen's manual updates, modules 1-5 as fallback.

| rule_id | 检查点 | 优先级规则 | 示例 |
|---|---|---|---|
| `override_teacher_first` | 老师明确改过的表达是否优先 | 老师规则高于公开写作指南 | 老师偏好 `main gap`，则不要因为某指南常用 `central question` 就改回 `central gap`。 |
| `override_project_domain` | 表达是否适合 LLZTO/phase-field/project proposal 语境 | 课题特定术语高于通用短语库 | `electrochemical weakening` 必须定义机制和参数，不能只用通用 phrasebank 模板。 |
| `override_no_mechanical_phrasebank` | 是否机械套短语 | 短语库只提供功能，不提供可直接复制的结论 | 把 `These findings suggest...` 改写成带对象、变量和证据等级的句子。 |
| `override_preserve_voice` | 是否保留 Stephen 自己的研究判断 | 不把文本全部改成模板腔 | 保留清楚、具体、有证据的原句，只修正风险词和逻辑边界。 |

Review order when using Lattice Wording:

1. 先查老师明确规则：replacement、style preference、concept warning、caption/citation。
2. 再查 module 6：是否有 teacher/project override。
3. 再查 module 1-5：clarity、argument、section wording、citation language、hedging。
4. 最后输出时分成：clear teacher-pattern issues、public-guide wording risks、content/concept evidence risks。
