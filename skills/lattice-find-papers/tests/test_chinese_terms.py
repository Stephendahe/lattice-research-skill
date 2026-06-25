import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_chinese_terms import find_undefined_english

class ChineseTermsTest(unittest.TestCase):
    def test_defined_term_passes(self):
        text = "固体电解质界面膜（solid electrolyte interphase, SEI）会影响枝晶生长（dendrite growth）。后续 SEI 可使用缩写。"
        self.assertEqual(find_undefined_english(text), [])
    def test_undefined_term_detected(self):
        self.assertIn("dendrite", find_undefined_english("SEI 会影响 dendrite growth。"))
if __name__ == "__main__":
    unittest.main()
