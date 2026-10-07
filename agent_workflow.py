import json
from typing import Literal

from agents import Agent, Runner
from pydantic import BaseModel, Field

from knowledge_base import GROUNDING_PACK

MODEL = "gpt-6-luna"

GROUNDING_INSTRUCTION = """
Use the curated grounding pack below as the primary assurance framework for this
portfolio demo. Do not contradict it with general model knowledge. If the pack
does not support a precise regulatory conclusion, say human verification is
required rather than filling the gap from memory.

""" + GROUNDING_PACK + "\n\n"

BASE_BOUNDARY = GROUNDING_INSTRUCTION + """
This is a fictional portfolio demonstration for UK financial-services assurance.
Do not make a legal determination, do not state that a breach definitely occurred,
and do not calculate or instruct redress. Distinguish evidence from inference.
Where information is missing, say that it is missing. Final judgement is human-led.

The case may include reviewer-entered fields and extracted text from uploaded
fictional/anonymised evidence. Treat those as the only case evidence. Never invent
a call, contact, vulnerability indicator, affordability assessment or support action.
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


class JourneyStep(BaseModel):
    stage: str
    status: Literal["Positive", "Concern", "Gap", "Not evidenced"]
    event: str
    evidence_source: str


class AssuranceResult(BaseModel):
    case_summary: str
    recommendation: Literal["Pass", "Further Work", "Escalate"]
    rationale: str
    agents_consulted: list[str] = Field(default_factory=list)
    decision_drivers: list[str] = Field(default_factory=list)
    customer_journey: list[JourneyStep] = Field(default_factory=list)
    findings: list[AssuranceFinding] = Field(default_factory=list)
    evidence_to_obtain: list[str] = Field(default_factory=list)
    human_review_note: str


affordability_agent = Agent(
    name="Affordability Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review affordability and financial-difficulty evidence. Check whether any arrangement
appears evidenced as sustainable, whether income/expenditure or equivalent evidence
is present, and whether temporary or changing circumstances were reflected. Trace
material findings to a supplied field or uploaded filename.
""",
)

vulnerability_agent = Agent(
    name="Vulnerability and Support Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review vulnerability, support needs and communication preferences across the supplied
journey evidence. Check whether identified needs were reflected in actions and contact.
Trace material findings to the supplied field or uploaded filename.
""",
)

evidence_agent = Agent(
    name="Evidence Challenge Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Challenge evidence quality and reviewer rationale. Look for contradictions,
unsupported conclusions, missing evidence and cases where customer agreement is
treated as proof of a fair outcome. Trace findings to supplied evidence.
""",
)

fos_examples_agent = Agent(
    name="FOS Illustrative Example Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use only published FOS examples in the curated grounding pack. Identify one only
where it genuinely helps a human reviewer understand an evidence or treatment theme.
It is illustrative, fact-specific and non-binding. Return the exact example and URL.
""",
)

regulatory_agent = Agent(
    name="Regulatory Reference Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use the curated FCA references in the grounding pack. Do not invent rule numbers,
quotes or URLs. Treat them as references for human verification, not proof of breach.
""",
)

lead_agent = Agent(
    name="Lead Consumer Duty Assurance Agent",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review the fictional Collections & Recoveries case as a customer journey, not just
as isolated text fields. Decide which specialist agents are useful and reconcile
their outputs into one assurance result.

CUSTOMER JOURNEY
Build a chronological or logical customer journey from supplied evidence. Include
stages where relevant such as:
- financial difficulty identified
- vulnerability / life event identified
- communication preference / support need recorded
- affordability assessment
- payment arrangement / forbearance
- subsequent contact
- wider support / signposting
- customer outcome
Use Positive, Concern, Gap or Not evidenced. Do not invent dates or events.

EVIDENCE TRACEABILITY
Every material finding must include evidence_refs. Source must be one of these exact
field labels or an uploaded filename:
Customer circumstances
Call / interaction notes
Vulnerability / support needs
Actions taken
Agent final rationale
Evidence must be a short excerpt or faithful paraphrase of supplied content.

When financial difficulty appears with vulnerability/life-event or unmet
communication preference, consult both regulatory and FOS specialists where relevant.
Do not force a source.

Record only specialists ACTUALLY called:
- Affordability
- Vulnerability & Support
- Evidence Challenge
- Regulatory Reference
- FOS Illustrative Example

Populate decision_drivers with the 2-3 most material reasons for the recommendation.

Recommend Pass only where evidence and rationale are coherent; Further Work where
evidence or rationale needs clarification; Escalate where there is a potentially
significant customer-outcome, vulnerability or contradiction concern.

Keep output concise, practical and human-led.
""",
    tools=[
        affordability_agent.as_tool(
            tool_name="review_affordability",
            tool_description="Review affordability and financial-difficulty evidence.",
        ),
        vulnerability_agent.as_tool(
            tool_name="review_vulnerability_support",
            tool_description="Review vulnerability, support needs and communication preferences.",
        ),
        evidence_agent.as_tool(
            tool_name="challenge_evidence_and_rationale",
            tool_description="Challenge evidence quality and unsupported rationale.",
        ),
        regulatory_agent.as_tool(
            tool_name="identify_regulatory_references",
            tool_description="Identify relevant FCA / Consumer Duty / CONC references.",
        ),
        fos_examples_agent.as_tool(
            tool_name="identify_fos_illustrative_examples",
            tool_description="Identify relevant published FOS illustrative examples.",
        ),
    ],
    output_type=AssuranceResult,
)


async def run_assurance(case: dict) -> AssuranceResult:
    uploaded = case.get("uploaded_evidence", "")
    prompt = """
Review the following fictional Collections & Recoveries case.

Use specialist tools where they add value. The final output is an assurance
recommendation for a human reviewer, not a customer decision.

CASE FIELDS:
""" + json.dumps({k: v for k, v in case.items() if k != "uploaded_evidence"}, indent=2)

    if uploaded.strip():
        prompt += """

UPLOADED JOURNEY EVIDENCE:
File boundaries are labelled. Use those filenames exactly when citing evidence.

""" + uploaded

    result = await Runner.run(lead_agent, prompt, max_turns=16)
    return result.final_output
