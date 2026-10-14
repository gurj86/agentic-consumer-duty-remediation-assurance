import copy
import io
import unittest

import httpx
from pypdf import PdfReader
from app import app


class FinalResponseTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")
        self.payload = {"human_decision": "Approve", "case_reference": "MF-DEMO",
                        "result": {"recommendation": "Uphold", "final_response_status": "Draft FRL - upheld",
                                   "final_response_draft": "Dear Alex,\nYour fictional complaint is upheld. <demo>",
                                   "redress_status": "Calculated", "redress_principal": "£1,300.32",
                                   "redress_interest": "£468.11", "redress_total": "£1,768.43",
                                   "redress_methodology_summary": "Fictional pre-calculated inputs only.",
                                   "rationale": "The rate-linked incentive was not disclosed.",
                                   "evidence_matrix": [{"item": "Commission schedule", "status": "Confirmed",
                                                        "source": "Fictional pack", "observation": "Rate discretion confirmed."}]}}

    async def asyncTearDown(self):
        await self.client.aclose()

    async def post(self, payload):
        return await self.client.post("/api/complaint-redress/final-response.pdf", json=payload)

    async def test_upheld_pdf_content_and_headers(self):
        response = await self.post(self.payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/pdf')
        self.assertIn('attachment;', response.headers['content-disposition'])
        text = '\n'.join(page.extract_text() for page in PdfReader(io.BytesIO(response.content)).pages)
        for expected in ('Dear Alex', '<demo>', '£1,300.32', '£468.11', '£1,768.43', 'Commission schedule',
                         'not disclosed', 'FICTIONAL PORTFOLIO DEMO ONLY', 'Financial Ombudsman Service'):
            self.assertIn(expected, text)

    async def test_reject_has_zero_redress(self):
        result = self.payload['result']
        result.update(recommendation='Reject', final_response_status='Draft FRL - not upheld',
                      final_response_draft='Your fictional complaint is not upheld.', redress_status='Not applicable')
        response = await self.post(self.payload)
        self.assertEqual(response.status_code, 200)
        text = ''.join(p.extract_text() for p in PdfReader(io.BytesIO(response.content)).pages)
        self.assertEqual(text.count('£0.00'), 3)
        self.assertNotIn('£1,768.43', text)

    async def test_blocks_unapproved_incomplete_and_uncalculated_cases(self):
        cases = [({'human_decision': 'Not recorded'}, {}), ({'human_decision': 'Escalate'}, {}),
                 ({'human_decision': 'Further Investigation'}, {}), ({'human_decision': ''}, {}),
                 ({}, {'recommendation': 'Further Investigation'}), ({}, {'recommendation': 'Escalate'}),
                 ({}, {'final_response_draft': ''}), ({}, {'final_response_status': 'Not generated - investigation incomplete'}),
                 ({}, {'redress_status': 'Pending human approval'}), ({}, {'redress_total': ''})]
        for outer, inner in cases:
            payload = copy.deepcopy(self.payload)
            payload.update(outer)
            payload['result'].update(inner)
            with self.subTest(outer=outer, inner=inner):
                self.assertEqual((await self.post(payload)).status_code, 409)
        self.assertEqual((await self.post({})).status_code, 409)


if __name__ == '__main__':
    unittest.main()
