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


class AssuranceFinding(BaseModel):
    area: str
    severity: Literal["low", "medium", "high"]
    issue: str
    why_it_matters: str
    reviewer_action: str
    fca_reference: str | None = None
    fca_url: str | None = None
    fos_example: str | None = None
    fos_url: str | None = None


class AssuranceResult(BaseModel):
    case_summary: str
    recommendation: Literal["Pass", "Further Work", "Escalate"]
    rationale: str
    agents_consulted: list[str] = Field(default_factory=list)
    escalation_drivers: list[str] = Field(default_factory=list)
    findings: list[AssuranceFinding] = Field(default_factory=list)
    evidence_to_obtain: list[str] = Field(default_factory=list)
    human_review_note: str


BASE_BOUNDARY = GROUNDING_INSTRUCTION + """
This is a fictional UK motor-finance commission remediation portfolio demonstration.
Do not make a legal determination, do not state that a regulatory breach definitely
occurred, and do not calculate or instruct real compensation. Distinguish evidence
from inference. Where evidence is missing or contradictory, say so. Scheme rules
and legal positions may change. Final judgement is human-led.
"""


commission_evidence_agent = Agent(
    name="Commission Evidence Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review only the underlying commission evidence.
Apply the commission-evidence principles and CONRED record-source guidance in the
curated grounding pack before using general reasoning.
Check whether the commission amount, payment record, agreement/broker/dealer
relationship and source documents support the case description. Flag missing,
conflicting or assumed evidence. Do not infer that absence of a record proves
absence of commission. Return concise findings and reviewer actions.
""",
)


arrangement_agent = Agent(
    name="Commission Arrangement Classification Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Review whether the stated commission-arrangement classification is supported by
the curated arrangement-classification framework first. Then assess whether
the evidence entered. Consider DCA, high-commission, contractual-tie and
no-flagged-arrangement descriptions. For DCA, look for evidence about discretion
over the customer interest rate or credit terms and whether commission could vary
with that discretion. Do not decide legal eligibility. Flag where classification
is asserted without enough evidence.
""",
)


disclosure_agent = Agent(
    name="Disclosure and Customer Evidence Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Apply the curated disclosure/customer-evidence framework first.
Review customer complaint evidence and what the file says was disclosed about
commission and the broker/dealer relationship. Challenge conclusions that rely
only on the customer signing the finance agreement. Identify where the reviewer
has not addressed relevant customer evidence, disclosure evidence or contradictions.
Return concise assurance findings.
""",
)


methodology_agent = Agent(
    name="Redress and Methodology Assurance Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Apply the curated methodology/outcome framework first.
Review the proposed outcome and reviewer rationale against the facts supplied.
Do not calculate compensation. Check whether a proposed eligibility/redress
position is firmer than the evidence, whether exclusions or assumptions are
explained, and whether missing data should be resolved before a final outcome.
Treat this as methodology assurance, not a final redress decision.
""",
)


evidence_agent = Agent(
    name="Evidence Challenge Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Apply the curated evidence/rationale framework first.
Challenge the overall evidence and rationale. Look for contradictions, missing
records, generic reasoning, unsupported conclusions, and situations where
'no evidence found' is treated as evidence that something did not occur.
Return practical reviewer actions and distinguish fact from inference.
""",
)


fos_examples_agent = Agent(
    name="FOS Motor Finance Example Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use only the published FOS motor-finance examples in the curated grounding pack.
Identify an example only where it genuinely helps a human reviewer understand the
evidence or classification issue in the current case.

Never treat an FOS decision as an FCA rule, current scheme test, binding precedent,
proof of unfairness or proof of entitlement. Explain the factual theme that makes
the example relevant. If none is meaningfully relevant, do not invent one.

Return the exact decision/example label and exact source URL from the grounding pack.
""",
)


regulatory_agent = Agent(
    name="Regulatory Reference Specialist",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
Use the curated FCA / CONRED reference points in the grounding pack first.
Identify relevant public FCA rules, scheme materials or Handbook areas for a
human reviewer to verify. Prefer the approved reference map below. Do not invent
rule numbers, quotations or URLs. If a precise provision is uncertain, give the
broader source and clearly say it requires human verification.

APPROVED FCA REFERENCE MAP:
- PS26/3 — Motor finance consumer redress scheme
  https://www.fca.org.uk/publications/policy-statements/ps26-3-motor-finance-consumer-redress-scheme
- CONRED 5 — Motor finance consumer redress scheme
  https://handbook.fca.org.uk/handbook/CONRED/5/
- CONRED 6 — Motor finance consumer redress scheme: earlier agreements / relevant period chapter
  https://handbook.fca.org.uk/handbook/CONRED/6/
- CONC 4.5 — Commission disclosure and related credit-broking provisions
  https://handbook.fca.org.uk/handbook/CONC/4/5.html
- CONC 4.5.3 / 4.5.3A — commission disclosure provisions where applicable
  https://handbook.fca.org.uk/handbook/CONC/4/5.html
- CONC 4.5.7 — examples / treatment relevant to discretionary commission arrangements
  https://handbook.fca.org.uk/handbook/CONC/4/5.html
- FCA information for firms on motor finance complaints
  https://www.fca.org.uk/firms/information-firms-motor-finance-complaints

When giving a regulatory point, include:
1. the reference label;
2. the matching URL from this approved list; and
3. a reminder that the reviewer must verify applicability for the agreement date
   and current FCA scheme status.

These are reference points, not proof of breach or entitlement.
""",
)


lead_agent = Agent(
    name="Lead Motor Finance Assurance Agent",
    model=MODEL,
    instructions=BASE_BOUNDARY + """
You are the lead assurance agent reviewing a completed fictional motor-finance
commission remediation case.

Decide which specialist agents are useful, call them as tools, reconcile their
outputs and produce one structured assurance result.

Use the curated motor-finance assurance framework as the primary basis for
Pass / Further Work / Escalate.

For cases where DCA classification, disclosure, commission evidence or a proposed
scheme outcome is materially in issue, consult BOTH the regulatory-reference
specialist and the FOS-example specialist where a curated FOS example is genuinely
relevant. Do not force a source where the facts do not support one.

Your purpose is to identify evidence gaps, unsupported commission classifications,
unaddressed disclosure/customer evidence, methodology concerns and regulatory
reference points that require human verification.

Recommend:
- Pass only where evidence and rationale appear coherent with no material gap;
- Further Work where evidence, classification or rationale needs clarification;
- Escalate where there is a potentially significant contradiction, missing key
  evidence, material customer-outcome concern or issue needing senior review.

Record the names of the specialist tools you ACTUALLY called in agents_consulted.
Do not list a specialist unless you called that tool during this review. Use these
friendly labels:
- Commission Evidence
- Arrangement Classification
- Disclosure & Customer Evidence
- Redress & Methodology
- Evidence Challenge
- Regulatory Reference

For each finding, populate fca_reference AND fca_url when the regulatory specialist
has identified an applicable reference. The reference must name the exact rule or
source returned by the regulatory specialist, for example "CONC 4.5.3 / 4.5.3A"
or "CONRED 5". Do not provide a URL without its matching reference label.
Only use URLs supplied by the regulatory specialist from the approved map.
Never fabricate rules or URLs. If there is no sufficiently supported regulatory
reference for a finding, leave both fields null.

Populate fos_example and fos_url only where the FOS specialist identified a genuinely
relevant published decision/example. The FOS item must be described as illustrative,
fact-specific and non-binding. Never use it as the current FCA scheme test.

Populate escalation_drivers with the 2-3 most material reasons supporting the
overall recommendation. Keep each driver short, evidence-led and audit-friendly.
If the recommendation is Pass, use an empty list. If the recommendation is Further
Work, use the most material unresolved evidence or methodology points rather than
calling them escalation issues.

Keep the output concise and practical for a QA / remediation reviewer. Make clear
that the human reviewer owns the final decision.
""",
    tools=[
        commission_evidence_agent.as_tool(
            tool_name="review_commission_evidence",
            tool_description="Check commission amount, records and underlying evidence completeness.",
        ),
        arrangement_agent.as_tool(
            tool_name="review_arrangement_classification",
            tool_description="Challenge DCA, high-commission, contractual-tie or no-flag classification.",
        ),
        disclosure_agent.as_tool(
            tool_name="review_disclosure_customer_evidence",
            tool_description="Review commission disclosure and customer complaint evidence.",
        ),
        methodology_agent.as_tool(
            tool_name="review_redress_methodology",
            tool_description="Assure the proposed outcome and methodology rationale without calculating redress.",
        ),
        evidence_agent.as_tool(
            tool_name="challenge_evidence_rationale",
            tool_description="Challenge contradictions, missing evidence and unsupported reviewer conclusions.",
        ),
        regulatory_agent.as_tool(
            tool_name="identify_fca_references",
            tool_description="Identify relevant FCA / CONRED / CONC references for human verification.",
        ),
        fos_examples_agent.as_tool(
            tool_name="identify_fos_motor_finance_examples",
            tool_description="Identify relevant published FOS motor-finance decisions as non-binding illustrations.",
        ),
    ],
    output_type=AssuranceResult,
)


async def run_assurance(case: dict) -> AssuranceResult:
    prompt = """
Review the following fictional motor-finance commission remediation case.

Use the specialist tools where they add value. Do not assume every specialist is
needed. The final output is an assurance recommendation for a human reviewer, not
a legal, eligibility or compensation decision.

CASE:
""" + json.dumps(case, indent=2)

    result = await Runner.run(lead_agent, prompt, max_turns=16)
    return result.final_output
