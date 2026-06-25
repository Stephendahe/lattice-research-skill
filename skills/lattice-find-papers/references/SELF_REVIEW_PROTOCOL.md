# 自我审核协议

final_report 生成前运行 self_review 和 honesty score。检查无证据 gap、摘要级结论冒充全文、相关冒充因果、缺全文却做实验审计、伪空白、英文术语未定义、缺少 Request 文献目录、缺少不确定项。

`logs/self_review.json` 必须包含 honesty_score、failed_checks、downgraded_claims、unsupported_claims_removed、requests_generated、resume_required、final_status。final_status 可选 complete_with_full_text、partial_due_to_missing_full_text、retrieval_only、blocked_waiting_for_user_files、failed_validation。
