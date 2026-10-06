# Agentic AI Consumer Duty & Remediation Assurance

A portfolio demonstration of a **multi-agent assurance workflow** for UK financial-services collections and remediation.

The initial use case is **Collections & Recoveries**. A lead assurance agent can call specialist agents to review:

- affordability and financial difficulty;
- vulnerability and customer support;
- communication preferences and customer-specific treatment;
- evidence gaps and rationale quality; and
- relevant FCA / CONC considerations.

The system then produces a structured assurance recommendation for **human review**.

## Why this is agentic

This project is different from a fixed rule-based dashboard. It uses the OpenAI Agents SDK so a lead agent can decide which specialist agents to call, use their findings, reconcile different issues and produce a final assurance summary.

The architecture follows a manager-style orchestration pattern:

1. **Lead Assurance Agent** receives the fictional case.
2. It decides which specialist reviews are needed.
3. It can call the **Affordability Agent**, **Vulnerability & Support Agent**, **Evidence Challenge Agent** and **Regulatory Reference Agent** as tools.
4. It combines the specialist outputs into a single assurance result.
5. A human reviewer makes the final decision: Pass / Further Work / Escalate.

## Important boundary

This is a personal portfolio prototype using fictional data only.

It does **not**:
- make regulatory or legal decisions;
- determine customer redress;
- replace approved firm methodology;
- replace human QA or compliance judgement; or
- contain real customer or employer information.

The agent output is a review aid. The human reviewer remains accountable for the final outcome.

## Run locally

Requires Python 3.10+ and an OpenAI API key.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Set your API key as an environment variable. **Do not put an API key in the code or commit it to GitHub.**

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-key-here"
```

macOS/Linux:

```bash
export OPENAI_API_KEY="your-key-here"
```

Then run:

```bash
uvicorn app:app --reload
```

Open http://127.0.0.1:8000

## Portfolio positioning

A simple way to describe this project:

> I designed a multi-agent Consumer Duty and remediation assurance workflow for Collections & Recoveries. A lead agent coordinates specialist reviews across affordability, vulnerability, evidence quality and regulatory considerations, then routes the output to a human reviewer for final judgement.

Built as a non-production demonstration of agentic AI use-case design, financial-services assurance and human-in-the-loop governance.
