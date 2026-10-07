"""
Curated grounding material for the Consumer Duty / Collections assurance demo.

This is intentionally small and controlled. It contains:
1. the portfolio assurance framework used by the older rule-based prototype; and
2. selected public FCA reference points used for human verification; and
3. selected published Financial Ombudsman Service examples used only as
   illustrations of evidence and fair-treatment themes.

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

FOS_EXAMPLE_KNOWLEDGE = """
PUBLISHED FOS EXAMPLES — ILLUSTRATIVE ONLY, NOT BINDING PRECEDENT

FOS vulnerability approach
The Financial Ombudsman Service says it considers the evidence from the consumer,
business and relevant third parties, the law/regulations/codes that applied, whether
the business knew or should have known the consumer was vulnerable, and what help
or support was offered or provided.
Source:
https://www.financial-ombudsman.org.uk/consumers/complaints-can-help/complaints/vulnerability

Maureen — grieving customer / vulnerability and repeated contact
Published FOS case study. The consumer said she was grieving and did not feel ready
to make financial decisions. FOS considered that the business had enough information
to recognise vulnerability and should have treated her fairly. This example is useful
for assurance themes around recognising bereavement, adapting treatment and avoiding
process-led pressure. It is not a rule and must not be treated as determinative of
another case.
Source:
https://www.financial-ombudsman.org.uk/businesses/resolving-complaint/case-studies/grieving-maureen-felt-pressured-buying-life-assurance

Glenn — collections communication / unexplained account action
Published FOS case study. The business had concerns about long-standing debt and was
entitled to take some account action, but FOS criticised failures to respond to the
customer's repayment proposals and failures to communicate important actions clearly.
This example is useful for assurance themes around responding to customer proposals,
clear communication and the impact of collections actions. It is not a rule and is
fact-specific.
Source:
https://www.financial-ombudsman.org.uk/businesses/resolving-complaint/case-studies/bank-transferred-money-but-didnt-tell-me

DRN-5852156 — affordability / vulnerability evidence
Published ombudsman decision concerning allegations of irresponsible lending,
unaffordability, vulnerability and collections treatment. Use only as an example that
affordability and vulnerability can require evidence-led consideration; do not infer
that its outcome applies to another customer.
Source:
https://www.financial-ombudsman.org.uk/decision/DRN-5852156.pdf

USAGE RULE
FOS examples are not FCA rules and are not binding precedent for this demo. They may
only be cited as illustrative examples of how evidence or customer-treatment issues
have been considered. Never say that a case must have the same outcome because it
resembles one of these examples.
"""

GROUNDING_PACK = (
    ASSURANCE_FRAMEWORK
    + "\n\n"
    + FCA_REFERENCE_KNOWLEDGE
    + "\n\n"
    + FOS_EXAMPLE_KNOWLEDGE
)
