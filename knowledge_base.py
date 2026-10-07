"""
Curated grounding material for the Consumer Duty / Collections assurance demo.

This is intentionally small and controlled. It contains:
1. the portfolio assurance framework used by the older rule-based prototype; and
2. selected public FCA reference points used for human verification.

It is not a substitute for a firm's approved methodology, current Handbook review,
legal advice, or a complete regulatory knowledge base.
"""

ASSURANCE_FRAMEWORK = """
PORTFOLIO ASSURANCE FRAMEWORK

Affordability / financial difficulty
- Look for evidence that any payment arrangement is sustainable and appropriate
  to the customer's current circumstances.
- Do not treat customer agreement to a payment amount as sufficient evidence of
  affordability on its own.
- Where income/expenditure or equivalent affordability evidence is absent, identify
  that as an evidence gap rather than assuming affordability.
- Consider whether temporary circumstances, reduced income, missed payments or a
  change in circumstances have been reflected in the proposed support.

Vulnerability / support
- Identify recorded indicators such as bereavement, health issues, life events,
  communication needs or other support requirements.
- Check whether the actions taken actually reflect those needs.
- Do not assume that recording a vulnerability indicator means appropriate support
  was provided.
- Check whether the customer's stated communication preference has been respected
  or, where it has not, whether the rationale is evidenced.

Evidence / rationale quality
- Distinguish facts in the case from reviewer inference.
- Challenge generic rationale that could apply to almost any case.
- Challenge conclusions that rely mainly on 'the customer agreed' or 'a plan was
  accepted' without supporting evidence of a fair outcome.
- Flag contradictions between the case facts, actions taken and reviewer rationale.
- Treat missing evidence as missing; do not convert absence of evidence into proof
  that an event or consideration did not exist.

Human assurance outcome
- Pass: evidence and rationale are coherent and no material assurance gap is found.
- Further Work: evidence or rationale needs clarification before assurance can be
  completed.
- Escalate: there is a potentially significant customer-outcome, vulnerability or
  evidence concern that warrants senior / specialist review.
"""

FCA_REFERENCE_KNOWLEDGE = """
CURATED FCA REFERENCE POINTS — HUMAN VERIFICATION REQUIRED

CONC 7.3.4
A firm must treat customers in or approaching arrears or in default with
forbearance and due consideration.
Source: https://handbook.fca.org.uk/handbook/conc7/conc7s3

CONC 7.3.4B
When determining appropriate forbearance and treating the customer with due
consideration, the firm must take account of the individual circumstances of the
customer of which it is or should be aware.
Source: https://handbook.fca.org.uk/handbook/conc7/conc7s3

CONC 7.2.1 / 7.2.2A
Policies and procedures should support fair and appropriate treatment of customers
the firm understands or reasonably suspects to be vulnerable. CONC 7.2.2A points
firms to FG21/1 when developing those policies and procedures.
Source: https://handbook.fca.org.uk/handbook/conc7/conc7s2

FG21/1
FCA guidance on the fair treatment of vulnerable customers. Use it as guidance
for understanding needs, appropriate support and fair outcomes; it is not itself
proof that a specific case breached a rule.
Source: https://www.fca.org.uk/publications/finalised-guidance/guidance-firms-fair-treatment-vulnerable-customers

PRIN 2A / Consumer Duty
For relevant retail customers, consider the cross-cutting obligation to avoid
causing foreseeable harm and the consumer support outcome. Applicability must be
checked against the current Handbook and case facts.
Source: https://handbook.fca.org.uk/handbook/prin2a

CONC 7 overall
Arrears, default and recovery requirements should be read together with the
Consumer Duty where applicable.
Source: https://handbook.fca.org.uk/handbook/conc7
"""

GROUNDING_PACK = ASSURANCE_FRAMEWORK + "\n\n" + FCA_REFERENCE_KNOWLEDGE
