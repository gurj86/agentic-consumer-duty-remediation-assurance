import unittest
from complaint_redress_completion import prepare, approve, pdf, unseal

CASE={'illustrative_redress_inputs':'actual flat rate 5.5%; fictional comparator flat rate 2.49%. Overpayment £1,300.32. Interest £468.11. Total £1,768.43.'}
RESULT={'recommendation':'Uphold','redress_status':'Calculated','missing_evidence':[],'rationale':'The evidenced rate-linked incentive was not adequately disclosed.','evidence_matrix':[{'item':'Commission schedule','status':'Confirmed'}]}
class CompletionTests(unittest.TestCase):
    def test_uphold(self):
        d=prepare(RESULT, CASE)
        self.assertEqual(d['redress_total'],'£1,768.43')
        self.assertIn('£1,300.32',d['final_response_draft'])
        with self.assertRaises(ValueError): pdf(d['review_token'])
        token=approve(d['review_token'],'Demo Reviewer')
        self.assertTrue(pdf(token).startswith(b'%PDF'))
        self.assertEqual(unseal(token)['reviewer'],'Demo Reviewer')
    def test_reject(self):
        d=prepare({**RESULT,'recommendation':'Reject'},CASE)
        self.assertEqual(d['redress_total'],'£0.00')
        self.assertIn('do not uphold',d['final_response_draft'])
    def test_incomplete(self):
        for outcome in ('Further Investigation','Escalate'):
            d=prepare({**RESULT,'recommendation':outcome},CASE)
            self.assertFalse(d['review_token'])
            self.assertFalse(d['final_response_draft'])
        self.assertFalse(prepare({**RESULT,'missing_evidence':['schedule']},CASE)['review_token'])
    def test_bad_calculation(self):
        self.assertFalse(prepare(RESULT,{'illustrative_redress_inputs':CASE['illustrative_redress_inputs'].replace('1,768.43','1,700.00')})['review_token'])
        self.assertFalse(prepare(RESULT,{})['review_token'])
    def test_tampering_and_reviewer(self):
        token=prepare(RESULT,CASE)['review_token']
        with self.assertRaises(ValueError): approve(token,' ')
        with self.assertRaises(ValueError): approve(token+'x','Reviewer')
if __name__=='__main__': unittest.main()
