# Agentic Financial Services Assurance Portfolio

A live portfolio demonstrating how **multi-agent AI workflows** can support assurance, remediation and quality review in UK financial services while keeping the final decision with a human reviewer.

The portfolio currently includes three agentic assurance workflows plus a governance and evaluation layer:

- **Consumer Duty / Collections Assurance**
- **Motor Finance Remediation Assurance**
- **Redress & Remediation Programme Assurance**
- **AI Governance & Evaluation Dashboard**

All scenarios are fictional or anonymised portfolio examples. The project is not connected to live customer systems and is not intended to make legal, regulatory, eligibility or compensation decisions.

---

## What this portfolio demonstrates

The aim is to show more than a single LLM reviewing a case.

Each workflow uses a **lead-agent / specialist-agent model**. The lead agent reads the case, decides which specialist reviewers are needed, calls them as tools, reconciles their findings and produces a structured recommendation for human review.

The portfolio demonstrates:

- multi-agent orchestration using the OpenAI Agents SDK;
- specialist reviewer roles rather than one general-purpose prompt;
- evidence-led reasoning and source traceability;
- controlled FCA / FOS grounding for human verification;
- document-evidence extraction from fictional or anonymised files;
- human-in-the-loop decisioning;
- downloadable assurance reporting;
- benchmark testing, versioning and evaluation controls; and
- clear boundaries between AI recommendation and human judgement.

---

## 1. Consumer Duty & Collections Assurance

A customer-journey assurance workflow for collections and recoveries cases.

The lead agent can coordinate specialist reviews covering:

- affordability and financial difficulty;
- vulnerability and support needs;
- communication preferences;
- evidence quality and reviewer rationale;
- FCA / CONC reference points; and
- selected FOS examples used only as fact-specific illustrations.

The workflow can also reconstruct the customer journey and highlight where treatment appears supported, unclear or not evidenced.

**Example flow**

Customer circumstances → Financial difficulty → Vulnerability / support → Affordability → Contact treatment → Outcome → Human review

**Key features**

- customer-journey reconstruction;
- evidence uploads;
- source-linked findings;
- affordability and vulnerability challenge;
- FCA / FOS grounding;
- Pass / Further Work / Escalate recommendation;
- human reviewer override; and
- PDF assurance report.

---

## 2. Motor Finance Remediation Assurance

An agreement and evidence-pack assurance workflow for motor-finance commission remediation.

The lead agent can coordinate specialist reviews covering:

- commission evidence;
- arrangement classification;
- DCA evidence;
- disclosure and customer evidence;
- redress / methodology assurance;
- evidence challenge;
- FCA / CONRED / CONC references; and
- selected FOS motor-finance examples.

The workflow is designed to distinguish between what the evidence actually establishes and what still requires further investigation.

**Example flow**

Agreement → Commission evidence → Arrangement type → Disclosure → Customer evidence → Scheme pathway → Assurance outcome

**Key features**

- agreement and evidence-pack upload;
- evidence sufficiency matrix;
- Confirmed / Unclear / Missing statuses;
- source traceability;
- DCA and commission challenge;
- regulatory grounding;
- human review; and
- PDF assurance report.

---

## 3. Redress & Remediation Programme Assurance

A programme-level assurance workflow designed to challenge whether a remediation exercise is genuinely ready for closure.

The specialist agents review:

- customer harm and root cause;
- population identification;
- data lineage and evidence;
- redress methodology;
- QA and outcome testing;
- governance and closure readiness; and
- regulatory reference points.

This moves the use case beyond reviewing a single customer file and into **remediation programme assurance**.

**Key features**

- programme-level risk assessment;
- evidence uploads and traceability;
- population challenge;
- data-lineage review;
- redress-methodology challenge;
- QA / outcome-testing review;
- RCA visualisation;
- closure-governance challenge;
- risk dashboard; and
- PDF assurance reporting.

---

## 4. AI Governance & Evaluation Dashboard

The Evaluation & Control Dashboard tests the existing agentic workflows rather than replacing them.

It runs controlled fictional benchmark cases where the expected outcome is defined **before** the model is called. The dashboard then compares the live agentic result against that expected outcome.

It measures:

- expected vs actual recommendation;
- evidence-traceability rate;
- regulatory-source-link coverage;
- response time;
- number of findings;
- specialist agents consulted;
- workflow / grounding / evaluation versions; and
- recent benchmark history.

A mismatch is not hidden or treated as a failure to be ignored. It is surfaced for **human investigation**.

This demonstrates a basic AI-governance principle:

> Build the workflow, test it, measure it, challenge it and keep the final judgement with a human reviewer.

---

## How the agents work together

The architecture uses a manager-style orchestration pattern:

1. The **Lead Agent** receives the fictional case.
2. It decides which specialist reviewers are relevant.
3. Specialist agents assess the case from their own area of expertise.
4. Their findings are returned to the lead agent.
5. The lead agent reconciles the evidence and produces one structured recommendation.
6. A human reviewer decides whether to accept, change or escalate the outcome.

The important distinction is that the lead agent does not simply send the same prompt to every specialist. It can choose which specialist tools are useful for the case.

---

## Controlled grounding

The workflows use curated grounding packs containing selected assurance principles and public regulatory reference points.

The agents are instructed to:

- use the controlled grounding material first;
- distinguish evidence from inference;
- avoid inventing rule references or source URLs;
- state when the supplied information does not support a precise conclusion; and
- treat regulatory and FOS material as reference points for human verification.

The portfolio is **not** connected to a live FCA Handbook feed, live FOS database or employer methodology.

A production implementation would require controlled firm methodology, access controls, validated source data, model governance, security review, audit retention and formal testing.

---

## Evidence and document handling

The portfolio can extract text from fictional or fully anonymised:

- PDF;
- DOCX;
- TXT;
- CSV; and
- XLSX files.

Uploaded evidence is used to support the current review. The public demo is not intended to be a document-management system.

Do **not** upload:

- real customer information;
- personal data;
- confidential employer material; or
- commercially sensitive case files.

Image-only / scanned PDFs are not supported in the public demo.

---

## Human-in-the-loop design

The AI does not own the final outcome.

Each workflow routes its recommendation to a human reviewer who can decide:

- **Pass**
- **Further Work**
- **Escalate**

This is deliberate. The system is positioned as an **assurance and evidence-challenge tool**, not an autonomous regulatory decision-maker.

---

## Technology

The portfolio uses:

- Python;
- FastAPI;
- OpenAI Agents SDK;
- structured Pydantic outputs;
- HTML / CSS / JavaScript front ends;
- server-side OpenAI API calls;
- document extraction for common office formats; and
- ReportLab PDF reporting.

The public code does not contain an API key. The key is supplied through the server environment.

---

## Run locally

Requires Python 3.10+ and an OpenAI API key.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:OPENAI_API_KEY="your-key-here"
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

Available routes:

```text
/consumer-duty
/motor-finance
/remediation
/evaluation
```

Never place an API key in the source code or commit it to GitHub.

---

## Portfolio positioning

A concise way to describe the project:

> I designed a portfolio of agentic financial-services assurance workflows where lead agents coordinate specialist reviewers across Consumer Duty, motor finance and remediation. The workflows challenge case evidence, use controlled regulatory grounding, trace findings back to source material and route structured recommendations to a human reviewer. I also built an Evaluation & Control Dashboard to benchmark the agents against pre-defined cases and surface mismatches for human investigation.

This is a **non-production portfolio demonstration** designed to show agentic workflow design, financial-services assurance knowledge, human-in-the-loop controls and AI evaluation principles.

---

## Important boundary

This project does **not**:

- provide legal or regulatory advice;
- make final customer or compensation decisions;
- replace approved firm methodology;
- connect to real customer systems;
- use real customer or employer data; or
- represent a production deployment for a client or financial-services firm.

The purpose is to demonstrate how agentic AI could support structured review and assurance while preserving human accountability.
