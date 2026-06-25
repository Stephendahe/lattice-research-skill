import csv, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_csv_headers import validate
from lattice_common import CSV_HEADERS

class ValidateCsvHeadersTest(unittest.TestCase):
    def test_valid_header(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "full_text_availability.csv"
            path.write_text(",".join(CSV_HEADERS["full_text_availability.csv"]) + "\n", encoding="utf-8")
            ok, _ = validate(path)
            self.assertTrue(ok)
if __name__ == "__main__":
    unittest.main()
