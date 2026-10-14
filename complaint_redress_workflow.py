import json
from typing import Literal
from agents import Agent, Runner
from pydantic import BaseModel, Field
from motor_finance_knowledge import MOTOR_FINANCE_GROUNDING_PACK

MODEL = "gpt-6-luna"

BOUNDARY = """
Fictional motor-finance complaint-to-redress portfolio demo only.
Do not determine real liability, scheme eligibility or compensation.
Use only the supplied fictional case evidence and fictional internal methodology.
Distinguish evidence from inference and state when evidence is missing.
Final decisions, redress and customer communications require human approval.

CONTROLLED MOTOR-FINANCE REFERENCE PACK:
""" + MOTOR_FINANCE_GROUNDING_PACK

class EvidenceRef(BaseModel):
    source: str
    evidence: str

class TimelineEvent(BaseModel):
    date_or_stage: str
    event: str
    source: str

class EvidenceItem(BaseModel):
    item: str
    status: Literal["Confirmed", "Unclear", "Missing"]
    source: str
    observation: str

class Finding(BaseModel):
    area: str
    severity: Literal["low", "medium", "high"]
    finding: str
    why_it_matters: str
    next_action: str
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)

class ComplaintWorkflowResult(BaseModel):
    complaint_summary: str
    complaint_category: str
    chronology: list[TimelineEvent] = Field(default_factory=list)
    evidence_matrix: list[EvidenceItem] = Field(default_factory=list)
    agents_consulted: list[str] = Field(default_factory=list)
    recommendation: Literal["Uphold", "Reject", "Further Investigation", "Escalate"]
    rationale: str
    findings: list[Finding] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    methodology_check: str
    redress_trigger: Literal["Not reached", "Illustrative calculation permitted", "Human methodology approval required"]
    redress_status: Literal["Not applicable", "Calculated", "Pending human approval"]
    redress_principal: str = ""
    redress_interest: str = ""
    redress_total: str = ""
    redress_methodology_summary: str = ""
    final_response_status: Literal["Not generated - investigation incomplete", "Draft FRL - upheld", "Draft FRL - not upheld"]
    final_response_draft: str
    human_review_note: str

def specialist(name, task):
    return Agent(name=name, model=MODEL, instructions=BOUNDARY + "\n" + task)

intake = specialist("Complaint Intake Specialist",
    "Extract the customer allegations, product and complaint themes without treating allegations as proven.")
chronology = specialist("Case Chronology Specialist",
    "Build a concise chronology from dated or clearly sequenced supplied evidence. Never invent dates.")
evidence = specialist("Evidence Pack Specialist",
    "Assess agreement, commission, arrangement mechanism, disclosure, customer evidence and case notes as Confirmed, Unclear or Missing.")
commission = specialist("Commission & Arrangement Specialist",
    "Review commission evidence and arrangement classification. A DCA flag alone is not conclusive if the underlying rate-setting mechanism is absent.")
disclosure = specialist("Disclosure & Customer Evidence Specialist",
    "Review actual disclosure and customer evidence. A signature alone is not proof of adequate commission disclosure.")
methodology = specialist("Internal Methodology Specialist",
    "Compare the evidence with the supplied fictional internal methodology and identify where human approval or missing inputs prevent a final outcome.")
response = specialist("Final Response Drafting Specialist",
    """Draft a concise customer-facing Final Response Letter (FRL) only when the complaint investigation is complete and the lead recommendation is Uphold or Reject.
The FRL must clearly state the final complaint outcome, the evidence considered, the main reasons, any completed illustrative redress outcome, and that this is a fictional portfolio draft requiring human approval before issue.
If the case is Further Investigation or Escalate, do not create an FRL; the case is not at final-response stage.""")

lead = Agent(
    name="Lead Complaint-to-Redress Agent",
    model=MODEL,
    instructions=BOUNDARY + """
Coordinate the fictional complaint from intake to outcome.
Use specialists where relevant and return an audit-friendly result covering complaint
classification, chronology, evidence sufficiency, findings, methodology check,
recommended outcome, completed illustrative redress where appropriate, and a draft final response.

FINAL RESPONSE RULE
A Final Response Letter is only appropriate when the investigation is complete.
- If recommendation is Uphold, set final_response_status to "Draft FRL - upheld" and draft an upheld final response.
- If recommendation is Reject, set final_response_status to "Draft FRL - not upheld" and draft a not-upheld final response.
- If recommendation is Further Investigation or Escalate, set final_response_status to "Not generated - investigation incomplete" and leave final_response_draft empty. Do not write a holding letter and call it a final response.

REDRESS RULE
For a completed upheld fictional case, use only the redress figures explicitly supplied in illustrative_redress_inputs and the fictional internal methodology. Do not invent or recalculate missing figures.
Where the supplied fictional methodology and figures are complete, set:
- redress_status = "Calculated"
- redress_trigger = "Illustrative calculation permitted"
and populate principal, interest, total and methodology summary exactly from the supplied fictional inputs.
For a completed rejected case use redress_status = "Not applicable".
For an incomplete investigation use redress_status = "Pending human approval" or "Not applicable" as appropriate.

Recommendations:
Uphold = evidence and fictional methodology support the complaint, subject to human approval.
Reject = evidence and methodology support rejection, subject to human approval.
Further Investigation = important evidence is missing or unclear.
Escalate = material contradiction or high-impact issue needs senior or specialist review.

Do not calculate real compensation or substitute current scheme rules. This portfolio demo may display a completed fictional redress outcome only where the fictional methodology and pre-calculated inputs are explicitly supplied. Every material finding should cite the supplied field or file.
""",
    tools=[
        intake.as_tool(tool_name="classify_complaint", tool_description="Classify the complaint and allegations."),
        chronology.as_tool(tool_name="build_chronology", tool_description="Build the case chronology."),
        evidence.as_tool(tool_name="assess_evidence", tool_description="Assess evidence sufficiency."),
        commission.as_tool(tool_name="review_commission", tool_description="Review commission and arrangement evidence."),
        disclosure.as_tool(tool_name="review_disclosure", tool_description="Review disclosure and customer evidence."),
        methodology.as_tool(tool_name="check_methodology", tool_description="Check the fictional internal methodology."),
        response.as_tool(tool_name="draft_response", tool_description="Draft the final response for human approval."),
    ],
    output_type=ComplaintWorkflowResult,
)

async def run_complaint_workflow(case: dict) -> ComplaintWorkflowResult:
    uploaded = case.get("uploaded_evidence", "")
    prompt = "Run this fictional complaint through the end-to-end workflow.\n\nCASE:\n" + json.dumps(
        {k:v for k,v in case.items() if k != "uploaded_evidence"}, indent=2
    )
    if uploaded.strip():
        prompt += "\n\nUPLOADED EVIDENCE:\n" + uploaded
    result = await Runner.run(lead, prompt, max_turns=24)
    return result.final_output
