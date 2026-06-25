# 日志落盘协议

所有过程日志写入 `runs/<run_id>/find_papers_outputs/logs/`，不要在用户界面输出流水账。`run.jsonl` 记录阶段事件；`retrieval.jsonl` 记录检索；`evidence_extraction.jsonl` 记录证据抽取；`validation.jsonl` 记录校验；`warnings.jsonl` 记录风险；`self_review.json` 记录最终自审。

JSONL 每行包含 timestamp、event、phase、level、message、data。日志必须可追加，不覆盖历史。
