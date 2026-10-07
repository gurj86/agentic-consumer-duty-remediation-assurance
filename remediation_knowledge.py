"""
Curated grounding material for the Agentic Redress & Remediation Assurance demo.

This is a controlled portfolio knowledge pack covering programme-level remediation
assurance. It is not a firm's approved methodology, legal advice, a regulatory
determination, or a substitute for current FCA Handbook review.
"""

REMEDIATION_ASSURANCE_FRAMEWORK = """
REDRESS & REMEDIATION ASSURANCE FRAMEWORK

Customer harm / root cause
- Define the harm clearly enough that a reviewer can identify who may have been
  affected, how the harm arose, and what evidence would demonstrate remediation.
- Distinguish the original control failure from downstream symptoms.
- Do not assume the absence of a complaint means the absence of customer harm.
- Check whether vulnerability or other customer characteristics could alter the
  impact or appropriate treatment.

Population identification
- Test whether inclusion and exclusion criteria logically follow from the defined
  harm and available data.
- Challenge populations built only from complaints where the underlying issue could
  also affect customers who did not complain.
- Check date windows, product / journey scope, exclusions, duplicates and edge cases.
- Where records are missing or unreliable, quantify the uncertainty and identify
  how potentially affected customers are being treated.
- Require a clear reconciliation between source population, exclusions, remediated
  cases and unresolved cases.

Data lineage / evidence
- Identify source systems, extracted fields, transformations, joins, assumptions and
  manual overrides used to reach the remediation outcome.
- Challenge unexplained missing values, estimated dates, proxies and inconsistent
  source records.
- Check whether important decision fields can be traced back to source evidence.
- Treat missing data as uncertainty, not as evidence that harm did not occur.
- Require reconciliations where data moves between source, calculation and payment
  / outcome files.

Redress methodology
- Check that the proposed calculation logic is linked to the defined customer harm.
- Check whether assumptions, proxies, interest / growth treatment, charges, timing
  and exceptions are documented and consistently applied.
- Do not calculate or instruct real compensation in this demo.
- Flag methodology that replaces case-specific evidence with averages without a
  documented reason or sensitivity assessment.
- Flag outcomes that are more certain than the underlying evidence.

QA / outcome testing
- Assess whether sampling is capable of finding the material failure modes in the
  population, not merely whether a sample exists.
- Consider population size, risk segmentation, exception cases and error severity.
- Check whether QA findings feed back into rework, methodology refinement and
  population expansion where necessary.
- A high completion percentage does not by itself demonstrate that outcomes are
  correct.

Governance / closure
- Check whether unresolved exceptions, disputed methodology, open data issues,
  payment failures or material QA findings are understood before closure.
- Require clear ownership, decision records and escalation routes for material
  judgement calls.
- Challenge closure based only on percentage complete, deadline pressure or absence
  of new complaints.
- Closure should be supported by evidence that the defined harm, population,
  methodology, execution and QA have been addressed to an appropriate standard.

Human assurance outcome
- Pass: the remediation design and evidence are coherent with no material assurance
  gap identified.
- Further Work: important evidence, methodology or governance points need resolution.
- Escalate: a material population, methodology, data, customer-harm or closure risk
  requires senior / specialist review.
"""

REGULATORY_GROUNDING = """
CURATED FCA REFERENCE POINTS — HUMAN VERIFICATION REQUIRED

PRIN 2A.2.5 — appropriate action where foreseeable harm is identified
Where a firm identifies that retail customers have suffered foreseeable harm from
its acts or omissions, the Consumer Duty requires appropriate action, including
redress where appropriate.
Source:
https://handbook.fca.org.uk/handbook/prin2a

PRIN 2A.2.8 — avoid causing foreseeable harm
Relevant as a high-level Consumer Duty reference when assessing the nature and
consequences of customer harm.
Source:
https://handbook.fca.org.uk/handbook/prin2a

PRIN 2A.10 — redress or other appropriate action
Sets out conduct relevant where a firm identifies foreseeable harm, including
investigation, assessment and appropriate remedial action / redress.
Source:
https://handbook.fca.org.uk/handbook/prin2a/prin2as10

DISP 1.4.1R — investigating, assessing and resolving complaints
Requires complaints to be investigated competently, diligently and impartially,
with fair, consistent and prompt assessment of the complaint and appropriate
remedial action or redress.
Source:
https://handbook.fca.org.uk/handbook/disp1/disp1s4

DISP 1.4.2G — relevant assessment factors
Includes available evidence and circumstances, similarities with other complaints,
relevant FCA / regulator / FOS guidance, and appropriate analysis of similar FOS
decisions.
Source:
https://handbook.fca.org.uk/handbook/disp1/disp1s4

PRIN 2A.8 — governance and culture
Consumer Duty should be reflected in governance, leadership and risk-control
arrangements, with retail customer outcomes as a central focus.
Source:
https://handbook.fca.org.uk/handbook/prin2a/prin2as8

USAGE RULE
These sources are regulatory reference points for a human reviewer. They do not,
by themselves, prescribe a specific remediation population, calculation methodology,
sample size or closure threshold. A firm's approved methodology and the facts of
the remediation remain necessary.
"""

REMEDIATION_GROUNDING_PACK = (
    REMEDIATION_ASSURANCE_FRAMEWORK
    + "\n\n"
    + REGULATORY_GROUNDING
)
