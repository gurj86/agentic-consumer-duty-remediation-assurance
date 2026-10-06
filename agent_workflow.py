import json
from typing import Literal

from agents import Agent, Runner
from pydantic import BaseModel, Field

MODEL = "gpt-6-luna"


class AssuranceFinding(BaseModel):
    area: str
    severity: Literal["low", "medium", "high"]
    issue: str
    why_it_matters: str
    reviewer_action: str
    fca_reference: str | None = None


class AssuranceResult(BaseModel):
    case_summary: str
    recommendation: Literal["Pass", "Further Work", "Escalate"]
    rationale: str
    findings: list[AssuranceFinding] = Field(default_factory=list)
    evidence_to_obtain: list[str] = Field(default_factory=list)
    human_review_note: str


BASE_BOUNDARY = """
This is a fictional portfolio demonstration for UK financial-services assurance.
Do not make a legal determination, do not state that a breach definitely occurred,
and do not calculate or instruct redress. Distinguish evidence from inference.
Where information is missing, say that it is missing. Final judgement is human-led.
"""


affordability_agent = Agent(
    name="Affordability Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review only affordability and financial-difficulty evidence.
Ask whether the proposed arrangement appears evidenced as sustainable,
whether income/expenditure or equivalent evidence is present, and whether
temporary or changing circumstances have been reflected. Return concise findings.
""",
)

vulnerability_agent = Agent(
    name="Vulnerability and Support Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review vulnerability, support needs and communication preferences.
Check whether identified needs appear reflected in the actions taken, whether
contact preferences have been considered, and whether support looks customer-specific.
Return concise findings and clearly separate fact from inference.
""",
)

evidence_agent = Agent(
    name="Evidence Challenge Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Challenge the quality of the case evidence and agent rationale.
Look for contradictions, unsupported conclusions, generic reasoning, missing
evidence, and cases where 'the customer agreed' is treated as proof of a fair outcome.
Return concise assurance findings and suggested reviewer actions.
""",
)

regulatory_agent = Agent(
    name="Regulatory Reference Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Identify relevant public FCA themes or Handbook areas that a human reviewer may
want to check, especially Consumer Duty, CONC arrears/default/recovery and FCA
vulnerability guidance. Do not invent rule numbers. If you are not confident in
a precise rule reference, give the broader FCA source/theme and say it should be
verified by the reviewer.
""",
)

lead_agent = Agent(
    name="Lead Consumer Duty Assurance Agent",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
You are the lead assurance agent. Review a completed collections/recoveries case.

Decide which specialist agents are useful, call them as tools, reconcile their
outputs and produce a single structured assurance result.

Your job is to identify potential evidence gaps, inconsistencies and customer-
outcome risks. Do not treat a specialist concern as a proven breach. Recommend:
- Pass only where the evidence and rationale appear coherent with no material gap;
- Further Work where evidence or rationale needs clarification;
- Escalate where there is a potentially significant customer-outcome concern,
  vulnerability issue, or material contradiction requiring senior review.

Keep the output practical for a second-line/QA reviewer and make clear that the
human reviewer owns the final decision.
""",
    tools=[
        affordability_agent.as_tool(
            tool_name="review_affordability",
            tool_description="Review affordability and financial-difficulty evidence in the case.",
        ),
        vulnerability_agent.as_tool(
            tool_name="review_vulnerability_support",
            tool_description="Review vulnerability, support needs and communication preferences.",
        ),
        evidence_agent.as_tool(
            tool_name="challenge_evidence_and_rationale",
            tool_description="Challenge evidence quality, inconsistencies and unsupported rationale.",
        ),
        regulatory_agent.as_tool(
            tool_name="identify_regulatory_references",
            tool_description="Identify relevant FCA/Consumer Duty/CONC references for human verification.",
        ),
    ],
    output_type=AssuranceResult,
)


async def run_assurance(case: dict) -> AssuranceResult:
    prompt = """
Review the following fictional Collections & Recoveries case.

You should use the specialist tools where they add value. The final output must
be an assurance recommendation for a human reviewer, not a customer decision.

CASE:
""" + json.dumps(case, indent=2)

    result = await Runner.run(lead_agent, prompt, max_turns=12)
    return result.final_output
