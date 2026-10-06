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
    fca_url: str | None = None


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
Identify relevant public FCA rules or guidance for the case and give the most
specific reference you can support. Prefer the approved source list below.
Do not invent rule numbers, quotes or URLs. If the facts do not support a precise
provision, use the broader section or guidance and say it requires human verification.

APPROVED FCA REFERENCE MAP:
- CONC 7.3.4 / 7.3.4B — forbearance, due consideration and individual circumstances
  https://handbook.fca.org.uk/handbook/conc7/conc7s3
- CONC 7.3.5 / 7.3.5I — examples of forbearance and keeping support appropriate
  https://handbook.fca.org.uk/handbook/conc7/conc7s3
- CONC 7.3.7A — free money guidance / debt-advice support where appropriate
  https://handbook.fca.org.uk/handbook/conc7/conc7s3
- CONC 7.3.13A — clear communications taking account of individual circumstances
  https://handbook.fca.org.uk/handbook/conc7/conc7s3
- CONC 7.2.1 / 7.2.2A — policies for fair treatment of vulnerable customers and FG21/1
  https://handbook.fca.org.uk/handbook/conc7/conc7s2
- FG21/1 — FCA Guidance for firms on the fair treatment of vulnerable customers
  https://www.fca.org.uk/publication/finalised-guidance/fg21-1.pdf
- PRIN 2A.2.8 — Consumer Duty: avoid causing foreseeable harm
  https://handbook.fca.org.uk/handbook/prin2a
- PRIN 2A.6 — Consumer Duty: consumer support outcome
  https://handbook.fca.org.uk/handbook/prin2a/prin2as6

When you provide a regulatory point to the lead agent, include BOTH:
1. the exact reference label; and
2. the matching URL from this approved list.

Treat these as references for a human reviewer to verify, not as proof of breach.
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

For each finding, populate fca_reference and fca_url when a relevant FCA source
has been identified by the regulatory specialist. Only use URLs supplied by that
specialist from the approved FCA reference map. Do not fabricate URLs.
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
