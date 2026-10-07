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
"""


class AssuranceFinding(BaseModel):
    area: str
    severity: Literal["low", "medium", "high"]
    issue: str
    why_it_matters: str
    reviewer_action: str
    regulatory_reference: str | None = None
    regulatory_url: str | None = None


class AssuranceResult(BaseModel):
    programme_summary: str
    recommendation: Literal["Pass", "Further Work", "Escalate"]
    rationale: str
    agents_consulted: list[str] = Field(default_factory=list)
    decision_drivers: list[str] = Field(default_factory=list)
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
Return concise findings and practical reviewer actions.
""",
)


data_agent = Agent(
    name="Data Lineage and Evidence Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review source systems, data fields, transformations, missing records, proxies,
estimated dates, reconciliations and traceability. Apply the curated data-lineage
framework. Treat missing data as uncertainty rather than proof of no harm.
""",
)


redress_agent = Agent(
    name="Redress Methodology Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review whether the described redress methodology is logically linked to the harm
and sufficiently evidenced. Challenge undocumented averages, proxies, timing
assumptions, inconsistent treatment and unexplained exceptions. Do not calculate
or instruct real customer compensation.
""",
)


qa_agent = Agent(
    name="QA and Outcome Testing Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review QA design, sampling, segmentation, exception testing, rework and feedback
loops. Apply the curated QA framework. Do not assume a high completion rate proves
that customer outcomes are correct.
""",
)


governance_agent = Agent(
    name="Governance and Closure Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review programme governance, unresolved issues, ownership, escalation and closure
readiness. Challenge closure based primarily on percentage complete, deadlines or
lack of new complaints where material evidence gaps remain.
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
    prompt = """
Review the following fictional financial-services remediation programme.

Use specialist tools where they add value. Do not assume every specialist is
required, but call all relevant specialists where the programme facts create
material assurance questions.

The output is for human remediation assurance / governance review. It is not a
legal decision, regulatory determination, final methodology approval or payment
instruction.

PROGRAMME:
""" + json.dumps(case, indent=2)

    result = await Runner.run(lead_agent, prompt, max_turns=18)
    return result.final_output
