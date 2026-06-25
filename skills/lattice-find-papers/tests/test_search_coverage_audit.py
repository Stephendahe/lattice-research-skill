import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_search_coverage import audit

class SearchCoverageAuditTest(unittest.TestCase):
    def test_single_source_risk(self):
        rows = [{"source_name": "OpenAlex", "covered_publishers": "A", "covered_journals": "J1", "method_types": "experiment", "mechanism_types": "defect", "variable_types": "pressure"}]
        risks = audit(rows)
        self.assertIn("单一数据库偏差", [r["risk"] for r in risks])
if __name__ == "__main__":
    unittest.main()
