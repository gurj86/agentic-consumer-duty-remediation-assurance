"""
Curated grounding material for the Motor Finance Commission assurance demo.

This pack is intentionally controlled. It contains:
1. a portfolio assurance framework for evidence, classification, disclosure and
   methodology challenge;
2. selected current FCA / CONRED / CONC reference points for human verification; and
3. selected published Financial Ombudsman Service decisions used only as
   fact-specific illustrations.

It is not a substitute for the current FCA Handbook, a firm's approved methodology,
legal advice or a complete FOS decision database.
"""

MOTOR_FINANCE_ASSURANCE_FRAMEWORK = """
MOTOR FINANCE ASSURANCE FRAMEWORK

Commission evidence
- Confirm what evidence actually establishes that commission was payable and, where
  relevant, the amount or a reasonable proxy.
- Prefer source evidence such as lender payment records, broker/dealer terms of
  business, commission schedules, rate tables and transaction-level records.
- A data flag may be useful evidence, but do not treat a flag or system label as a
  complete substitute for the underlying arrangement evidence where that evidence
  is needed to support the conclusion.
- Treat missing source records as an evidence gap. Do not convert absence of a
  document into proof that commission, discretion or disclosure did not exist.

Arrangement classification
- Distinguish discretionary commission arrangements from fixed / flat fee
  arrangements and from other relevant arrangements.
- For DCA classification, look for evidence that the broker/dealer had discretion
  over the customer interest rate or relevant credit terms and that commission could
  vary with that discretion.
- Challenge a DCA conclusion that relies only on a flag with no evidence of the
  rate-setting mechanism.
- Challenge a non-DCA conclusion where the file has not established the actual
  commission mechanism.
- Where the current FCA redress scheme applies, check relevant-arrangement rules,
  exclusions and the agreement date rather than assuming every commission payment
  falls within the same treatment.

Disclosure / customer evidence
- Identify what the customer says they understood about the dealer/broker role and
  commission.
- Identify what disclosure evidence is actually present in the file.
- Do not treat the customer's signature on the finance agreement as, by itself,
  proof that commission was adequately disclosed or that the customer understood
  the nature of the arrangement.
- Separate the existence of a disclosure document from evidence that its contents
  addressed the relevant commission arrangement.

Methodology / outcome assurance
- Check whether the proposed scheme classification or redress pathway follows from
  the evidence actually present.
- Do not calculate or instruct compensation in this portfolio demo.
- Where key inputs are missing, recommend evidence retrieval or further work rather
  than forcing a final outcome.
- Distinguish current FCA scheme rules from older complaint-handling or historical
  FOS reasoning.
- Where a current FCA rule is subject to legal challenge, suspension or change,
  surface that status and require human verification before relying on it.

Evidence / rationale quality
- Distinguish facts from reviewer inference.
- Flag generic rationale that could apply to many cases.
- Flag conclusions that are firmer than the evidence.
- Flag contradictions between lender records, broker records, customer evidence and
  the reviewer's stated conclusion.
- Do not treat 'no evidence found' as evidence that an event did not happen.

Human assurance outcome
- Pass: evidence and rationale are coherent and no material assurance gap is found.
- Further Work: evidence, classification or rationale needs clarification.
- Escalate: a material contradiction, potentially significant customer-outcome issue,
  or key missing evidence requires senior / specialist review.
"""

FCA_MOTOR_FINANCE_KNOWLEDGE = """
CURATED FCA / HANDBOOK REFERENCE POINTS — HUMAN VERIFICATION REQUIRED

PS26/3 — Motor finance consumer redress scheme
The FCA published the motor finance consumer redress scheme in March 2026. Use this
as the current policy source for the scheme and implementation context.
Source:
https://www.fca.org.uk/publications/policy-statements/ps26-3-motor-finance-consumer-redress-scheme

CONRED 5 — Motor finance commission consumer redress scheme (2014-2024)
Use CONRED 5 for scheme cases within its scope. Confirm the agreement date and
current applicability before relying on a provision.
Source:
https://handbook.fca.org.uk/handbook/conred5

CONRED 5.1.3 — meaning of commission / evidence of commission payable
Commission includes financial consideration payable by a lender to a credit broker
in connection with a specific motor finance agreement. The rules allow actual
commission paid in financial records to be used as a reasonable proxy in relevant
circumstances.
Source:
https://handbook.fca.org.uk/handbook/conred5

CONRED 5.2.19 — identifying a relevant arrangement
Relevant arrangements can include discretionary commission, high commission and
tied arrangements, subject to stated exceptions. Do not assume every commission
payment is a relevant arrangement.
Source:
https://handbook.fca.org.uk/handbook/conred5/conred5s2

CONRED 5.2.23 / 5.2.24 — insufficient information / obtaining records
These provisions address evidence expectations and steps for identifying scheme
cases and relevant arrangements where records are insufficient.
Source:
https://handbook.fca.org.uk/handbook/conred5/conred5s2

CONRED 5 Annex 1 — relevant records and information
The annex identifies sources such as lender/broker arrangements, rate and terms
documents, commission arrangements, minimum/maximum interest rates and other records
that may be relevant to determining scheme status, disclosure and redress.
Source:
https://handbook.fca.org.uk/handbook/conred5/conred5s12

CONRED 6 — earlier-agreement motor finance scheme chapter
Use only where the agreement falls within CONRED 6 scope. Confirm dates and current
scheme application.
Source:
https://handbook.fca.org.uk/handbook/conred6

CONC 4.5 — commission disclosure / credit-broking provisions
Historical applicability depends on the agreement date and the rule in force at the
time. Use only after checking the relevant version and facts.
Source:
https://handbook.fca.org.uk/handbook/CONC/4/5.html

CURRENT-STATUS WARNING
Some CONRED redress provisions have been subject to Upper Tribunal challenge and
the Handbook flags some provisions as partially or wholly suspended pending further
order or final determination. Never present a redress calculation or final entitlement
without checking the current FCA position.
Source:
https://handbook.fca.org.uk/handbook/conred5/conred5s4
"""

FOS_MOTOR_FINANCE_EXAMPLES = """
PUBLISHED FOS MOTOR FINANCE EXAMPLES — ILLUSTRATIVE ONLY, NOT BINDING PRECEDENT

FOS motor finance commission guidance
FOS explains that commission complaints can involve different commission models and
that current handling is affected by the FCA scheme. Use this as context for the
complaint type, not as a rule.
Source:
https://www.financial-ombudsman.org.uk/businesses/resolving-complaint/complaints-deal/consumer-credit/car-finance/complaints-about-commission

DRN-4188284 — discretionary commission / rate-setting evidence
Published FOS decision involving a discretionary commission arrangement. The decision
examined the broker's discretion to choose the interest rate, the link between rate
and commission, the underlying commission agreement and whether any extra work
justified the differential commission. Useful as an illustration of why the actual
rate-setting mechanism and source documents matter. It is fact-specific and not a
binding precedent.
Source:
https://www.financial-ombudsman.org.uk/decision/DRN-4188284.pdf

DRN-4326581 — DCA / conflict and customer fairness
Published FOS decision involving a 2018 conditional-sale agreement and a commission
model linking broker commission to the interest rate while allowing the broker
discretion to adjust that rate. Useful as an illustration of evidence needed to
understand the commission mechanism and customer impact. It is fact-specific and
must not be treated as the current FCA scheme test.
Source:
https://www.financial-ombudsman.org.uk/decision/DRN-4326581.pdf

DRN-4218349 — fixed fee / non-DCA evidence
Published FOS decision where evidence showed a fixed fee and a predetermined
interest rate, with no broker discretion to alter the rate for more commission.
Useful as a counter-example: not every commission arrangement is a DCA, and the
classification should follow the underlying evidence rather than the complaint label.
It is fact-specific and not binding precedent.
Source:
https://www.financial-ombudsman.org.uk/decision/DRN-4218349.pdf

FOS DECISION-DATABASE WARNING
FOS states that individual ombudsman decisions are based on the unique circumstances
of each case and are not a definitive statement of the law or the Service's approach.
Source:
https://www.financial-ombudsman.org.uk/businesses/resolving-complaint/ombudsman-decisions

USAGE RULE
Use FOS decisions only as factual illustrations. Never say that a case must have the
same outcome because it resembles one of these decisions. Current FCA / CONRED scheme
rules and the firm's approved methodology take priority for a scheme review.
"""

MOTOR_FINANCE_GROUNDING_PACK = (
    MOTOR_FINANCE_ASSURANCE_FRAMEWORK
    + "\n\n"
    + FCA_MOTOR_FINANCE_KNOWLEDGE
    + "\n\n"
    + FOS_MOTOR_FINANCE_EXAMPLES
)
