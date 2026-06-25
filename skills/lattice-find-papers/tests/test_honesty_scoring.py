import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from score_answer_honesty import score_text

class HonestyScoringTest(unittest.TestCase):
    def test_material_insufficiency_adds_credit(self):
        result = score_text("# 报告\n## 证据边界\n材料不足，需要全文。\nRequest 文献目录")
        self.assertGreaterEqual(result["honesty_score"], 100)
    def test_pseudo_gap_penalty(self):
        result = score_text("需要搭建统一框架。")
        self.assertLess(result["honesty_score"], 100)
if __name__ == "__main__":
    unittest.main()
