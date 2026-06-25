# 核心表字段

所有 CSV 字段见 `assets/*_template.csv` 和 `schemas/*.schema.json`。必填字段至少包括各表主键和可追溯来源字段。

| 表 | 主键 | 关键字段 | 允许值提示 |
|---|---|---|---|
| papers_master | paper_id | title、year、doi、source_url、inclusion_decision、verification_status、access_level | inclusion_decision、verification_status、access_level 使用 schema enum |
| search_coverage_audit | source_name + query_block | query_string、results_count、coverage_warning | results_count 可为整数 |
| full_text_availability | paper_id | access_status、access_level、missing_sections、needs_user_upload、local_library_checked、local_library_source、local_match_confidence、local_full_text_status、local_supplement_status | access_status 使用全文状态 enum；本地字段只记录全文可得性子步骤 |
| full_text_requests | request_id | why_full_text_needed、needed_sections、missing_for_tasks、priority、resume_checkpoint、local_library_checked、local_library_result、local_resolution_status | priority: high/medium/low；local_resolution_status 记录 Request 前本地检查结果 |
| evidence_spans | evidence_id | source_text、source_location、claim_type、confidence | confidence: high/medium/low/speculative |
| variable_relations | relation_id | variable_A、variable_B、relation_type、access_level、confidence | comparability_status 使用 enum |
| mechanism_comparison | mechanism_id | causal_chain、supporting_evidence、limitations | access_level 和 confidence 必填 |
| mechanism_conflicts | conflict_id | shared_question、A_claim、B_claim、contradiction_type | access_level_sufficient 标记证据是否足够 |
| experiment_pipeline_audit | audit_id | material_source、test_protocol、unreported_variables、severity | severity 使用 enum |
| normalization_blockers | blocker_id | missing_item、why_it_blocks_comparison、is_core_variable、severity | blocker_level 可写变量/流程/尺度/数据处理 |
| citation_audit | claim_id | claim_sentence、citation、support_level、problem、action | support_level 使用 enum |
| pseudo_gap_hits | gap_id | phrase、why_risky、rewrite_action | 来自伪空白库 |
