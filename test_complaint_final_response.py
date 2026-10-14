import copy
import io
import time
import unittest
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient, ASGITransport
from pypdf import PdfReader
import app

RESULT = {"recommendation": "Uphold", "final_response_status": "Draft FRL - upheld", "complaint_summary": "Rate-linked commission was not explained.", "rationale": "The supplied agreement and commission schedule evidence a rate-linked incentive that was not adequately disclosed.", "missing_evidence": [], "evidence_matrix": [{"item": "Commission schedule", "status": "Confirmed", "source": "Fictional schedule", "observation": "Dealer selected a higher rate and earned higher commission."}], "redress_status": "Calculated", "redress_trigger": "Illustrative calculation permitted", "redress_principal": "\u00a31,300.32", "redress_interest": "\u00a3468.11", "redress_total": "\u00a31,768.43", "redress_methodology_summary": "Pre-calculated overpayments against the fictional comparator, plus fictional simple interest."}


class FinalResponseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(transport=ASGITransport(app=app.app), base_url="http://test")
        app._complaint_cases.clear()
        app._complaint_cases["test"] = {"result": copy.deepcopy(RESULT), "created": time.time(), "approved_at": None, "reference": "MF-DEMO-TEST"}

    async def asyncTearDown(self):
        await self.client.aclose()

    async def decision(self, decision="Approve"):
        return await self.client.post("/api/complaint-redress/decision", json={"case_id": "test", "decision": decision})

    async def download(self):
        return await self.client.post("/api/complaint-redress/final-response-pdf", json={"case_id": "test", "decision": "Download"})

    async def test_approval_required_and_revocable(self):
        self.assertEqual((await self.download()).status_code, 409)
        self.assertEqual((await self.decision()).status_code, 200)
        response = await self.download()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/pdf")
        text = " ".join(p.extract_text() for p in PdfReader(io.BytesIO(response.content)).pages)
        for expected in ["\u00a31,768.43", "Evidence considered", "Reasons for our decision", "Financial Ombudsman", "FICTIONAL"]:
            self.assertIn(expected, text)
        await self.decision("Escalate")
        self.assertEqual((await self.download()).status_code, 409)

    async def test_incomplete_outcomes_never_download(self):
        for outcome in ["Further Investigation", "Escalate"]:
            app._complaint_cases["test"]["result"]["recommendation"] = outcome
            self.assertEqual((await self.decision()).status_code, 409)
            self.assertEqual((await self.download()).status_code, 409)

    async def test_reject_zero_even_with_stale_upheld_figures(self):
        result = app._complaint_cases["test"]["result"]
        result.update(recommendation="Reject", final_response_status="Draft FRL - not upheld", redress_status="Not applicable")
        self.assertEqual((await self.decision()).status_code, 200)
        text = " ".join(p.extract_text() for p in PdfReader(io.BytesIO((await self.download()).content)).pages)
        self.assertIn("\u00a30.00", text)
        self.assertNotIn("\u00a31,768.43", text)

    async def test_gaps_and_bad_redress_block_approval(self):
        for changes in [{"missing_evidence": ["Agreement"]}, {"redress_total": "\u00a31,700.00"}, {"redress_status": "Pending human approval"}, {"redress_principal": "invented"}]:
            app._complaint_cases["test"]["result"] = {**copy.deepcopy(RESULT), **changes}
            self.assertEqual((await self.decision()).status_code, 409)

    async def test_expired_or_unknown_case(self):
        app._complaint_cases["test"]["created"] -= 3601
        self.assertEqual((await self.decision()).status_code, 404)
        self.assertEqual((await self.download()).status_code, 404)


if __name__ == "__main__":
    unittest.main()
