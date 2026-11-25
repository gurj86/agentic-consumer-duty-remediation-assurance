"""Offline control tests: no API calls. Run python -m unittest test_bifd -v."""
import unittest
from unittest.mock import AsyncMock, patch
from types import SimpleNamespace
from bifd_workflow import (BiFDInput, Finding, Evidence, QUESTIONS, SPECIALISTS,
    SpecialistResult, Summary, Governance, validate_input, validate_findings, overall, run_bifd,
    KNOWLEDGE, AGENT_SOURCES, grounding)

def case(text="Recorded monthly disposable income of £120."):
    return BiFDInput(agreement="PCP",synthetic_confirmed=True,case={"investigation":text})

def finding(q="Q05",status="Pass",excerpt="£120",source="CASE.investigation"):
    return Finding(question_id=q,status=status,rationale="Illustrative assessment",
        evidence=[Evidence(source=source,excerpt=excerpt)],reference="CONC 7.3",reviewer_action="Verify.")

class Controls(unittest.TestCase):
    def test_source_assignment(self):
        self.assertEqual(set(AGENT_SOURCES), {name for name, _ in SPECIALISTS} | {"Lead QA","Independent governance"})
        for name, ids in AGENT_SOURCES.items():
            self.assertTrue(ids)
            self.assertTrue(set(ids) <= set(KNOWLEDGE))
            for key in ids:
                self.assertIn(KNOWLEDGE[key][2],grounding(name))
    def test_reference_not_supplied(self):
        f=finding()
        f.reference="DRN-5634627"
        self.assertEqual(validate_findings([f],["Q05"],validate_input(case()),AGENT_SOURCES["Affordability"])[0].status,"Further review")
    def test_reference_supplied(self):
        f=finding()
        f.reference="DRN-6129262"
        self.assertEqual(validate_findings([f],["Q05"],validate_input(case()),AGENT_SOURCES["Affordability"])[0].status,"Pass")
    def test_fabricated_quote(self):
        self.assertEqual(validate_findings([finding(excerpt="£900")],["Q05"],validate_input(case()))[0].status,"Further review")
    def test_fake_source(self):
        self.assertEqual(validate_findings([finding(source="CALL-9.notes")],["Q05"],validate_input(case()))[0].status,"Further review")
    def test_real_quote(self):
        self.assertEqual(validate_findings([finding()],["Q05"],validate_input(case()))[0].status,"Pass")
    def test_no_evidence(self):
        f=finding();f.evidence=[]
        self.assertEqual(validate_findings([f],["Q05"],validate_input(case()))[0].status,"Further review")
    def test_duplicate(self):
        self.assertEqual(validate_findings([finding(),finding()],["Q05"],validate_input(case()))[0].status,"Further review")
    def test_missing(self):
        self.assertEqual(validate_findings([],["Q05"],validate_input(case()))[0].status,"Further review")
    def test_incomplete_overall(self):
        self.assertEqual(overall([finding()]),"Further review")
    def test_complete_pass(self):
        self.assertEqual(overall([finding(q) for q in QUESTIONS]),"Pass")
    def test_fail_precedence(self):
        self.assertEqual(overall([finding(q,"Fail" if q=="Q05" else "Pass") for q in QUESTIONS]),"Fail")
    def test_all_na_not_pass(self):
        self.assertEqual(overall([finding(q,"Not applicable") for q in QUESTIONS]),"Further review")
    def test_pii(self):
        for text in ["demo@example.invalid","07123 456789","123456789"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                validate_input(case(text))
    def test_empty(self):
        with self.assertRaises(ValueError):validate_input(case(""))
    def test_confirmation(self):
        with self.assertRaises(ValueError):
            BiFDInput(agreement="PCP",synthetic_confirmed=False,case={})
    def test_extra_field(self):
        with self.assertRaises(ValueError):
            BiFDInput(agreement="PCP",synthetic_confirmed=True,case={"name":"fictional"})
    def test_call_source(self):
        c=BiFDInput(agreement="PCP",synthetic_confirmed=True,case={},calls=[{"notes":"Fictional call"}])
        self.assertEqual(validate_input(c),{"CALL-1.notes":"Fictional call"})

class Workflow(unittest.IsolatedAsyncioTestCase):
    async def test_governance_rebuilds_summary(self):
        outputs=[SpecialistResult(findings=[finding(q) for q in ids]) for _,ids in SPECIALISTS]
        outputs += [Summary(rationale="Draft",actual_harm="Unsupported claim",potential_harm="Unknown",feedback="Draft"),
                    Governance(concerns=["Unsupported harm"],challenged_questions=["Q05"],summary_supported=False)]
        with patch("bifd_workflow.Runner.run",new=AsyncMock(side_effect=[SimpleNamespace(final_output=x) for x in outputs])) as runner:
            result=await run_bifd(case())
        self.assertEqual(runner.await_count,8)
        self.assertEqual(result.agent_sources,AGENT_SOURCES)
        for call in runner.await_args_list:
            agent=call.args[0]
            self.assertIn(grounding(agent.name),agent.instructions)
        self.assertEqual(result.recommendation,"Further review")
        self.assertEqual(len(result.findings),20)
        self.assertIn("unresolved",result.summary.feedback.lower())
        self.assertEqual([f.question_id for f in result.original_challenged_findings],["Q05"])
        self.assertEqual(result.original_challenged_findings[0].status,"Pass")
        self.assertNotIn("Unsupported claim",result.summary.actual_harm)
    async def test_unchallenged_failure_retained(self):
        outputs=[SpecialistResult(findings=[finding(q,"Fail" if q=="Q04" else "Pass") for q in ids]) for _,ids in SPECIALISTS]
        outputs += [Summary(rationale="Draft",actual_harm="Unsupported claim",potential_harm="Unknown",feedback="Draft"),
                    Governance(concerns=["Unsupported harm"],challenged_questions=["Q05"],summary_supported=False)]
        with patch("bifd_workflow.Runner.run",new=AsyncMock(side_effect=[SimpleNamespace(final_output=x) for x in outputs])):
            result=await run_bifd(case())
        self.assertEqual(result.recommendation,"Fail")
        self.assertIn("Q04",result.summary.feedback)
        self.assertNotIn("Unsupported claim",result.summary.actual_harm)
    async def test_model_failure_stops_review(self):
        with patch("bifd_workflow.Runner.run",new=AsyncMock(side_effect=RuntimeError("simulated outage"))):
            with self.assertRaises(RuntimeError):await run_bifd(case())

if __name__=="__main__":unittest.main()
