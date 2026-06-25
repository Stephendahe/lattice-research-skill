# 上传全文后续跑示例

1. 用户上传 `P001_example_full_text.pdf`。
2. 运行 `python scripts/match_uploaded_full_text.py runs/<run_id> --files P001_example_full_text.pdf`。
3. 运行 `python scripts/resume_run.py runs/<run_id>`。
4. 从 `phase_10_structure_round` 继续，不重复多源检索和覆盖审计。
5. final_report 标注“本轮基于补充全文继续执行”。
