import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from self_review import review

class SelfReviewRulesTest(unittest.TestCase):
    def test_pseudo_gap_fails(self):
        result = review("需要搭建统一框架。\n## 不确定项\n材料不足。", False)
        self.assertIn("pseudo_gap_phrase", result["failed_checks"])
if __name__ == "__main__":
    unittest.main()
