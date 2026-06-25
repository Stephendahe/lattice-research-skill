import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_full_text_request_queue import build_requests, infer_request_pdf_dir, render_doi_list_md, update_availability_with_local_checks

class RequestQueueTest(unittest.TestCase):
    def test_builds_request_for_abstract_only(self):
        rows = [{"paper_id": "P1", "title": "Example", "doi": "unknown", "access_status": "abstract_only", "access_level": "L1_title_abstract", "needs_user_upload": "true", "request_priority": "high", "missing_sections": "Methods"}]
        req = build_requests(rows, [])
        self.assertEqual(req[0]["priority"], "high")
        self.assertEqual(req[0]["request_id"], "R001")

    def test_request_pdf_dir_is_inferred_from_request_queue_output(self):
        with tempfile.TemporaryDirectory() as td:
            output_csv = Path(td) / "run-test" / "find_papers_outputs" / "request_queue" / "full_text_requests.csv"
            self.assertEqual(infer_request_pdf_dir(output_csv), (Path(td) / "run-test" / "request_PDF").resolve())

    def test_renders_doi_list_as_two_sections(self):
        requests = [{
            "title": "Example Paper",
            "authors": "Zhang et al.",
            "year": "2024",
            "doi": "https://doi.org/10.1234/Example",
            "source_url": "",
        }]
        md = render_doi_list_md(requests)
        self.assertIn("## DOI\n\n- 10.1234/example", md)
        self.assertIn("## Web Links", md)
        self.assertIn("- Title: Example Paper", md)
        self.assertIn("  Authors: Zhang et al.", md)
        self.assertIn("  Year: 2024", md)
        self.assertIn("  Link: https://doi.org/10.1234/example", md)

    def test_build_requests_preserves_author_metadata_for_doi_list(self):
        rows = [{"paper_id": "P1", "title": "Example", "doi": "10.1234/example", "access_status": "abstract_only", "access_level": "L1_title_abstract", "needs_user_upload": "true", "request_priority": "high", "missing_sections": "Methods"}]
        papers = [{"paper_id": "P1", "title": "Example", "authors": "Zhang and Li", "year": "2024", "doi": "10.1234/example", "source_url": "https://publisher.example/paper", "inclusion_decision": "include_core"}]
        req = build_requests(rows, papers)
        md = render_doi_list_md(req)
        self.assertIn("  Authors: Zhang and Li", md)
        self.assertIn("  Link: https://publisher.example/paper", md)

    def test_local_pdf_resolves_main_text_request(self):
        with tempfile.TemporaryDirectory() as td:
            pdf = Path(td) / "Example.pdf"
            pdf.write_text("placeholder", encoding="utf-8")
            availability = [{"paper_id": "P1", "title": "Example", "doi": "unknown", "access_status": "abstract_only", "access_level": "L1_title_abstract", "needs_user_upload": "true", "request_priority": "high", "missing_sections": "Methods"}]
            papers = [{"paper_id": "P1", "title": "Example", "inclusion_decision": "include_core"}]
            updated, stats = update_availability_with_local_checks(availability, papers, local_pdf_dir=td)
            self.assertEqual(stats["resolved"], 1)
            self.assertEqual(updated[0]["local_full_text_status"], "pdf_found")
            self.assertEqual(build_requests(updated, papers), [])

    def test_background_only_is_not_requested(self):
        rows = [{"paper_id": "P2", "title": "Background", "doi": "unknown", "access_status": "abstract_only", "access_level": "L1_title_abstract", "needs_user_upload": "true", "request_priority": "low", "missing_sections": "Methods"}]
        papers = [{"paper_id": "P2", "title": "Background", "inclusion_decision": "background_only"}]
        self.assertEqual(build_requests(rows, papers), [])

    def test_local_pdf_with_missing_supplement_requests_only_supplement(self):
        with tempfile.TemporaryDirectory() as td:
            Path(td, "Example_Core.pdf").write_text("placeholder", encoding="utf-8")
            availability = [{"paper_id": "P1", "title": "Example Core", "doi": "unknown", "access_status": "abstract_only", "access_level": "L1_title_abstract", "needs_user_upload": "true", "request_priority": "high", "missing_sections": "Supplementary"}]
            papers = [{"paper_id": "P1", "title": "Example Core", "inclusion_decision": "include_core"}]
            updated, _ = update_availability_with_local_checks(availability, papers, local_pdf_dir=td)
            req = build_requests(updated, papers)
            self.assertEqual(req[0]["needed_sections"], "Supplementary")
            self.assertEqual(req[0]["local_resolution_status"], "partially_resolved_missing_supplement")

    def test_local_supplement_found_still_requests_main_pdf(self):
        with tempfile.TemporaryDirectory() as td:
            source_list = Path(td) / "sources.csv"
            source_list.write_text(
                "doi,title,local_full_text_status,local_library_source\n"
                "10.1234/example,Example Core,supplement_found,local_supplement_folder\n",
                encoding="utf-8",
            )
            availability = [{"paper_id": "P1", "title": "Example Core", "doi": "10.1234/example", "access_status": "abstract_only", "access_level": "L1_title_abstract", "needs_user_upload": "true", "request_priority": "high", "missing_sections": "Full text;Supplementary"}]
            papers = [{"paper_id": "P1", "title": "Example Core", "doi": "10.1234/example", "inclusion_decision": "include_core"}]
            updated, _ = update_availability_with_local_checks(availability, papers, local_source_list=str(source_list))
            req = build_requests(updated, papers)
            self.assertEqual(updated[0]["local_supplement_status"], "supplement_found")
            self.assertEqual(req[0]["needed_sections"], "Full text / main PDF")
            self.assertIn("主文 PDF", req[0]["user_action"])
if __name__ == "__main__":
    unittest.main()
