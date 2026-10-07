import json
from typing import Literal

from agents import Agent, Runner
from pydantic import BaseModel, Field

from remediation_knowledge import REMEDIATION_GROUNDING_PACK

MODEL = "gpt-6-luna"

GROUNDING_INSTRUCTION = """
Use the curated remediation grounding pack below as the primary assurance basis.
Do not contradict it with general model knowledge. Where the pack does not support
a precise conclusion, state that human verification or approved firm methodology
is required rather than inventing a rule.

""" + REMEDIATION_GROUNDING_PACK + "\n\n"

BASE_BOUNDARY = GROUNDING_INSTRUCTION + """
This is a fictional UK financial-services remediation portfolio demonstration.
Do not make legal determinations, final regulatory conclusions, scheme eligibility
decisions or real compensation instructions. Distinguish evidence from inference.
Final judgement and remediation governance remain human-led.

The case may include reviewer-entered fields and extracted text from uploaded
fictional/anonymised evidence files. Treat those as the only case evidence.
Never claim a document contains something unless that text is actually supplied.
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
    regulatory_reference: str | None = None
    regulatory_url: str | None = None


class RiskRating(BaseModel):
    area: Literal[
        "Customer Harm",
        "Population",
        "Data Lineage",
        "Redress Methodology",
        "QA / Outcome Testing",
        "Governance / Closure",
    ]
    rating: Literal["Low", "Medium", "High"]
    reason: str


class RootCauseAnalysis(BaseModel):
    root_cause: str
    customer_harm: str
    population_risk: str
    data_issue: str
    methodology_impact: str
    qa_issue: str
    closure_risk: str


class AssuranceResult(BaseModel):
    programme_summary: str
    recommendation: Literal["Pass", "Further Work", "Escalate"]
    rationale: str
    agents_consulted: list[str] = Field(default_factory=list)
    decision_drivers: list[str] = Field(default_factory=list)
    risk_dashboard: list[RiskRating] = Field(default_factory=list)
    root_cause_analysis: RootCauseAnalysis
    findings: list[AssuranceFinding] = Field(default_factory=list)
    evidence_to_obtain: list[str] = Field(default_factory=list)
    human_review_note: str


harm_population_agent = Agent(
    name="Customer Harm and Population Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review the definition of customer harm and the affected population. Apply the
curated customer-harm and population framework. Challenge weak inclusion/exclusion
criteria, complaint-only populations, untested edge cases and unreconciled totals.
For any finding, identify the supplied source field or uploaded file and a short
supporting excerpt or faithful paraphrase.
""",
)


data_agent = Agent(
    name="Data Lineage and Evidence Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review source systems, data fields, transformations, missing records, proxies,
estimated dates, reconciliations and traceability. Apply the curated data-lineage
framework. Treat missing data as uncertainty rather than proof of no harm.
Trace material findings back to the supplied field or uploaded filename.
""",
)


redress_agent = Agent(
    name="Redress Methodology Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review whether the described redress methodology is logically linked to the harm
and sufficiently evidenced. Challenge undocumented averages, proxies, timing
assumptions, inconsistent treatment and unexplained exceptions. Do not calculate
or instruct real customer compensation. Trace material findings to supplied
evidence.
""",
)


qa_agent = Agent(
    name="QA and Outcome Testing Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review QA design, sampling, segmentation, exception testing, rework and feedback
loops. Apply the curated QA framework. Do not assume a high completion rate proves
that customer outcomes are correct. Trace material findings to supplied evidence.
""",
)


governance_agent = Agent(
    name="Governance and Closure Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review programme governance, unresolved issues, ownership, escalation and closure
readiness. Challenge closure based primarily on percentage complete, deadlines or
lack of new complaints where material evidence gaps remain. Trace material findings
to supplied evidence.
""",
)


regulatory_agent = Agent(
    name="Regulatory Reference Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use only the curated FCA / Handbook reference points in the grounding pack when
providing specific regulatory references. Give the exact reference label and exact
URL. Do not invent rule numbers or imply that a high-level rule prescribes a
specific sample size, population methodology or calculation formula. State where
approved firm methodology or human verification is required.
""",
)


lead_agent = Agent(
    name="Lead Redress and Remediation Assurance Agent",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
You are the lead assurance agent reviewing a fictional remediation programme.

Decide which specialist agents are useful, call them as tools, reconcile their
outputs and produce one structured programme-assurance result.

Use the curated framework as the primary basis for Pass / Further Work / Escalate.

Consider:
- whether the harm and population are complete and logically defined;
- whether source data and transformations are traceable;
- whether the redress methodology is supported by evidence;
- whether QA / outcome testing can detect material errors; and
- whether the programme has enough evidence to support closure.

EVIDENCE TRACEABILITY
For every material finding, populate evidence_refs with one or more sources from
the case. Source must be either one of these exact field labels:
Customer harm / root cause
Population identification
Data lineage / evidence
Redress methodology
QA / outcome testing
Governance / proposed closure
or an uploaded filename exactly as shown in the uploaded evidence text.
The evidence text must be a short excerpt or faithful paraphrase of supplied
content. Never invent evidence.

RISK DASHBOARD
Return exactly one risk rating for each of the six areas. Base the rating on the
supplied evidence and specialist review, not on arbitrary scoring.

RCA FLOW
Create a concise root-cause flow that connects the stated root cause to customer
harm, population risk, data issue, methodology impact, QA issue and closure risk.
If a stage is not evidenced, explicitly say "Not evidenced in supplied material"
rather than inventing it.

For material findings with a relevant curated FCA source, consult the regulatory
specialist and populate regulatory_reference and regulatory_url. Never invent a
source.

Record only the specialist agents ACTUALLY called in agents_consulted using these
friendly labels:
- Harm & Population
- Data Lineage
- Redress Methodology
- QA & Outcome Testing
- Governance & Closure
- Regulatory Reference

Populate decision_drivers with the 2-3 most material reasons for the overall
recommendation. If Pass, the list may be empty.

Keep the output concise and useful for a second-line, remediation assurance or
programme-governance reviewer. The human reviewer owns the final decision.
""",
    tools=[
        harm_population_agent.as_tool(
            tool_name="review_harm_population",
            tool_description="Challenge customer-harm definition and affected-population identification.",
        ),
        data_agent.as_tool(
            tool_name="review_data_lineage",
            tool_description="Challenge source data, transformations, missing fields, proxies and reconciliations.",
        ),
        redress_agent.as_tool(
            tool_name="review_redress_methodology",
            tool_description="Assure redress logic, assumptions, proxies and exception handling without calculating compensation.",
        ),
        qa_agent.as_tool(
            tool_name="review_qa_outcomes",
            tool_description="Review sampling, QA coverage, outcome testing, rework and feedback loops.",
        ),
        governance_agent.as_tool(
            tool_name="review_governance_closure",
            tool_description="Assess programme governance, unresolved issues and closure readiness.",
        ),
        regulatory_agent.as_tool(
            tool_name="identify_remediation_regulatory_references",
            tool_description="Identify curated FCA / Consumer Duty / DISP references for human verification.",
        ),
    ],
    output_type=AssuranceResult,
)


async def run_assurance(case: dict) -> AssuranceResult:
    uploaded = case.get("uploaded_evidence", "")
    prompt = """
Review the following fictional financial-services remediation programme.

Use specialist tools where they add value. Do not assume every specialist is
required, but call all relevant specialists where the programme facts create
material assurance questions.

The output is for human remediation assurance / governance review. It is not a
legal decision, regulatory determination, final methodology approval or payment
instruction.

PROGRAMME FIELDS:
""" + json.dumps({k: v for k, v in case.items() if k != "uploaded_evidence"}, indent=2)

    if uploaded.strip():
        prompt += """

UPLOADED EVIDENCE TEXT:
The text below was extracted from user-supplied fictional/anonymised files. File
boundaries are labelled. Cite those filenames exactly when using them as evidence.

""" + uploaded

    result = await Runner.run(lead_agent, prompt, max_turns=20)
    return result.final_output
