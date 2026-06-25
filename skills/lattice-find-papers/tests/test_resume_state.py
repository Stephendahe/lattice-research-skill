import json, subprocess, sys, tempfile, unittest
from pathlib import Path

class ResumeStateTest(unittest.TestCase):
    def test_init_run_creates_resume_state(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            subprocess.check_call([sys.executable, str(root / "scripts" / "init_run.py"), "--topic", "测试主题", "--runs-dir", td, "--run-id", "run-test"])
            state = json.loads((Path(td) / "run-test" / "resume_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["next_resume_phase"], "phase_0_task_intake")
            doi_list = Path(td) / "run-test" / "request_PDF" / "doi_list.md"
            self.assertTrue(doi_list.exists())
            self.assertEqual(doi_list.read_text(encoding="utf-8"), "## DOI\n\n## Web Links\n")
            output_root = Path(td) / "run-test" / "find_papers_outputs"
            self.assertTrue((output_root / "tables" / "papers_master.csv").exists())
            self.assertTrue((output_root / "request_queue" / "full_text_requests.csv").exists())
            self.assertTrue((output_root / "outputs" / "mechanism_map.md").exists())
            self.assertFalse((Path(td) / "run-test" / "tables").exists())
            self.assertFalse((Path(td) / "run-test" / "request_queue").exists())
if __name__ == "__main__":
    unittest.main()
