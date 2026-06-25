# 断点续跑协议

每次执行创建 `runs/<run_id>/`，根目录只保留 `run_manifest.json`、`resume_state.json` 和 `request_PDF/`。Lattice Find Papers 的副产物全部写入 `find_papers_outputs/`，其中包含 request_queue、logs、tables、outputs、inputs 和 intermediate_tables。

`resume_state.json` 必须记录 run_id、topic、completed_phases、blocked_phases、blocking_requests、next_resume_phase、required_user_files、tables_completed、tables_partial、last_updated。

用户上传新 PDF、补充材料或数据后，读取上一轮 resume_state；匹配上传文件与 request_id、paper_id、DOI、title；更新 full_text_availability；从 next_resume_phase 继续；不重复已完成检索和已验证表格；追加 logs；在 final_report 标注“本轮基于补充全文继续执行”。

如果用户后来把文献加入 Zotero、本地 PDF 文件夹、本地补充材料文件夹或手动路径清单，可以重新执行全文可得性检查。重新检查只针对仍需全文的候选文献，不重复完整检索，不扫描 background_only/exclude 文献；high/medium 置信度匹配可更新全文状态，low/tentative 匹配进入人工确认。更新后从 `next_resume_phase` 或对应 `resume_checkpoint` 继续。

匹配优先级：DOI 精确匹配、paper_id 匹配、标题规范化匹配、作者 + 年份匹配、用户手动指定。
