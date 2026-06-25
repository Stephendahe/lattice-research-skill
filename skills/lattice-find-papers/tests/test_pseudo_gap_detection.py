import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from detect_pseudo_gap_phrases import detect

class PseudoGapTest(unittest.TestCase):
    def test_detects_gap_phrase(self):
        hits = detect("需要搭建统一框架来实现数据归一化。")
        self.assertGreaterEqual(len(hits), 2)
if __name__ == "__main__":
    unittest.main()
