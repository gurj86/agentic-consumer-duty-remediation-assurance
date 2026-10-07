import json
from typing import Literal

from agents import Agent, Runner
from pydantic import BaseModel, Field

from motor_finance_knowledge import MOTOR_FINANCE_GROUNDING_PACK

MODEL = "gpt-6-luna"

GROUNDING_INSTRUCTION = """
Use the curated motor-finance grounding pack below as the primary assurance basis
for this portfolio demo. Do not contradict it with general model knowledge. If the
pack does not support a precise regulatory conclusion, say human verification is
required rather than filling the gap from memory.

""" + MOTOR_FINANCE_GROUNDING_PACK + "\n\n"

BASE_BOUNDARY = GROUNDING_INSTRUCTION + """
This is a fictional UK motor-finance commission remediation portfolio demonstration.
Do not make a legal determination, do not state that a regulatory breach definitely
occurred, and do not calculate or instruct real compensation. Distinguish evidence
from inference. Where evidence is missing or contradictory, say so. Scheme rules
and legal positions may change. Final judgement is human-led.

The case may include reviewer-entered fields and extracted text from uploaded
fictional/anonymised evidence files. Treat those as the only case evidence.
Never claim an agreement, commission schedule, disclosure or lender record says
something unless it is actually present in the supplied material.
"""


class EvidenceRef(BaseModel):
    source: str
    evidence: str


class AssuranceFinding(BaseModel):
    area: str
    severity: Literal["low", "medium", "high"]
    issue: str
    why_it_matters: str
    reviewer_action: str
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    fca_reference: str | None = None
    fca_url: str | None = None
    fos_example: str | None = None
    fos_url: str | None = None


class EvidenceMatrixRow(BaseModel):
    evidence_required: str
    status: Literal["Confirmed", "Unclear", "Missing"]
    source: str
    gap_or_observation: str
    agent_conclusion: str


class AgreementEvidenceFlow(BaseModel):
    agreement: str
    commission_evidence: str
    arrangement_type: str
    disclosure: str
    customer_evidence: str
    scheme_pathway: str
    assurance_outcome: str


class AssuranceResult(BaseModel):
    case_summary: str
    recommendation: Literal["Pass", "Further Work", "Escalate"]
    rationale: str
    agents_consulted: list[str] = Field(default_factory=list)
    escalation_drivers: list[str] = Field(default_factory=list)
    evidence_matrix: list[EvidenceMatrixRow] = Field(default_factory=list)
    agreement_evidence_flow: AgreementEvidenceFlow
    findings: list[AssuranceFinding] = Field(default_factory=list)
    evidence_to_obtain: list[str] = Field(default_factory=list)
    human_review_note: str


commission_evidence_agent = Agent(
    name="Commission Evidence Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review the underlying commission evidence, including uploaded evidence where present.
Apply the commission-evidence principles and CONRED record-source guidance in the
curated grounding pack. Check whether the amount, payment record, broker/dealer
relationship and source records support the case description. Trace any finding to
a supplied field or uploaded filename and do not infer that absence proves no commission.
""",
)

arrangement_agent = Agent(
    name="Commission Arrangement Classification Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review whether the stated commission-arrangement classification is supported.
For DCA, look for evidence of discretion over the customer interest rate or credit
terms and whether commission could vary with that discretion. Do not treat a system
flag alone as conclusive where the underlying mechanism is not evidenced. Trace
material findings to supplied evidence.
""",
)

disclosure_agent = Agent(
    name="Disclosure and Customer Evidence Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review what the supplied agreement, disclosure records and customer evidence actually
show about commission and the broker/dealer relationship. Do not treat a signature
alone as proof of adequate commission disclosure or customer understanding. Trace
material findings to the supplied field or uploaded filename.
""",
)

methodology_agent = Agent(
    name="Redress and Methodology Assurance Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review the proposed outcome and methodology rationale against the supplied evidence.
Do not calculate compensation. Challenge outcomes that are firmer than the evidence,
unsupported assumptions or missing inputs that should be resolved before a final
scheme outcome. Trace findings to supplied evidence.
""",
)

evidence_agent = Agent(
    name="Evidence Challenge Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Challenge contradictions, missing records, generic reasoning, unsupported conclusions
and situations where 'no evidence found' is treated as proof that something did not
occur. Where multiple documents conflict, identify the conflict and sources.
""",
)

fos_examples_agent = Agent(
    name="FOS Motor Finance Example Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use only the published FOS motor-finance examples in the curated grounding pack.
Identify an example only where it genuinely helps explain the evidence or
classification issue. Treat it as fact-specific and non-binding, never as the
current FCA scheme test. Return the exact label and source URL from the pack.
""",
)

regulatory_agent = Agent(
    name="Regulatory Reference Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use only supported FCA / CONRED / CONC reference points from the curated grounding
pack and approved map. Do not invent rule numbers, quotes or URLs. Remind the human
reviewer to verify applicability for agreement date and current scheme status.
""",
)

lead_agent = Agent(
    name="Lead Motor Finance Assurance Agent",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review the fictional motor-finance evidence pack and decide which specialists to call.
Reconcile their outputs into one human-reviewable assurance result.

EVIDENCE TRACEABILITY
Every material finding must include evidence_refs. Source must be one of these field
labels or an uploaded filename exactly as labelled in the evidence text:
Agreement details
Commission evidence
Arrangement classification
Disclosure / customer evidence
Proposed outcome
Reviewer rationale
The evidence value must be a short excerpt or faithful paraphrase. Never invent evidence.

EVIDENCE SUFFICIENCY MATRIX
Build a concise matrix covering, where relevant:
- executed agreement / agreement terms
- commission payment / amount
- commission schedule or broker/dealer terms
- rate-setting discretion / DCA mechanism
- commission disclosure evidence
- customer evidence / complaint account
- scheme classification inputs
Use Confirmed, Unclear or Missing. "Confirmed" means the supplied material genuinely
supports the point, not merely that a system flag exists.

AGREEMENT EVIDENCE FLOW
Create a concise flow:
Agreement -> Commission evidence -> Arrangement type -> Disclosure -> Customer
evidence -> Scheme pathway -> Assurance outcome.
If a stage is not evidenced, say so rather than filling the gap.

For material DCA, disclosure, commission or scheme-outcome issues, use regulatory
and FOS specialists where relevant. FCA/FOS material is for human verification,
not proof of breach or entitlement.

Record only specialists ACTUALLY called using:
- Commission Evidence
- Arrangement Classification
- Disclosure & Customer Evidence
- Redress & Methodology
- Evidence Challenge
- Regulatory Reference
- FOS Illustrative Example

Recommend Pass only with coherent evidence and no material gap; Further Work where
evidence/classification needs clarification; Escalate where key evidence is missing,
contradictory or creates a material customer-outcome concern.

Keep output concise, audit-friendly and human-led.
""",
    tools=[
        commission_evidence_agent.as_tool(
            tool_name="review_commission_evidence",
            tool_description="Check commission records and source evidence completeness.",
        ),
        arrangement_agent.as_tool(
            tool_name="review_arrangement_classification",
            tool_description="Challenge DCA and other commission-arrangement classification.",
        ),
        disclosure_agent.as_tool(
            tool_name="review_disclosure_customer_evidence",
            tool_description="Review disclosure, signed agreement and customer evidence.",
        ),
        methodology_agent.as_tool(
            tool_name="review_redress_methodology",
            tool_description="Assure proposed outcome and methodology without calculating compensation.",
        ),
        evidence_agent.as_tool(
            tool_name="challenge_evidence_rationale",
            tool_description="Challenge contradictions, missing evidence and unsupported rationale.",
        ),
        regulatory_agent.as_tool(
            tool_name="identify_fca_references",
            tool_description="Identify curated FCA / CONRED / CONC references for verification.",
        ),
        fos_examples_agent.as_tool(
            tool_name="identify_fos_motor_finance_examples",
            tool_description="Identify relevant published FOS motor-finance illustrations.",
        ),
    ],
    output_type=AssuranceResult,
)


async def run_assurance(case: dict) -> AssuranceResult:
    uploaded = case.get("uploaded_evidence", "")
    prompt = """
Review the following fictional motor-finance commission remediation case.

Use specialist tools where they add value. The final output is an assurance
recommendation for a human reviewer, not a legal, eligibility or compensation decision.

CASE FIELDS:
""" + json.dumps({k: v for k, v in case.items() if k != "uploaded_evidence"}, indent=2)

    if uploaded.strip():
        prompt += """

UPLOADED EVIDENCE TEXT:
File boundaries are labelled. Use those filenames exactly in evidence references.

""" + uploaded

    result = await Runner.run(lead_agent, prompt, max_turns=20)
    return result.final_output
