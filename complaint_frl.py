"""PDF export for human-approved, completed fictional complaint outcomes."""
import io
from xml.sax.saxutils import escape

from fastapi import HTTPException
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def build_final_response_pdf(payload):
    result = payload.get("result")
    if not isinstance(result, dict) or payload.get("human_decision") != "Approve":
        raise HTTPException(409, "Human approval of a completed outcome is required.")
    outcome = result.get("recommendation")
    expected = {"Uphold": "Draft FRL - upheld", "Reject": "Draft FRL - not upheld"}
    if (outcome not in expected or result.get("final_response_status") != expected[outcome]
            or not str(result.get("final_response_draft") or "").strip()):
        raise HTTPException(409, "The investigation must be complete before downloading a final response.")
    if outcome == "Uphold" and (result.get("redress_status") != "Calculated" or
            any(not str(result.get(k) or "").strip() for k in
                ("redress_principal", "redress_interest", "redress_total", "redress_methodology_summary"))):
        raise HTTPException(409, "Complete the illustrative redress calculation before downloading.")

    stream = io.BytesIO()
    styles = getSampleStyleSheet()
    story = []

    def paragraph(text, style="BodyText"):
        story.append(Paragraph(escape(str(text)).replace("\n", "<br/>"), styles[style]))
        story.append(Spacer(1, 3 * mm))

    paragraph("Final Response Letter", "Title")
    paragraph("FICTIONAL PORTFOLIO DEMO ONLY - Not for issue to a real customer.")
    paragraph("Case reference: " + str(payload.get("case_reference") or "Fictional demonstration case"))
    paragraph("Human reviewer: Approve (demo only). Outcome: " + outcome, "Heading2")
    paragraph(result["final_response_draft"])
    paragraph("Evidence considered", "Heading2")
    for row in result.get("evidence_matrix", []):
        paragraph(f"{row.get('item', '')}: {row.get('status', '')}. {row.get('observation', '')} Source: {row.get('source', '')}")
    paragraph("Reasons for the outcome", "Heading2")
    paragraph(result.get("rationale", ""))
    paragraph("Illustrative redress breakdown", "Heading2")
    for label, key in (("Principal / overpayment", "redress_principal"),
                       ("Compensatory interest", "redress_interest"), ("Total", "redress_total")):
        paragraph(label + ": " + (str(result[key]) if outcome == "Uphold" else "£0.00"))
    if outcome == "Uphold":
        paragraph(result["redress_methodology_summary"])
    paragraph("Next steps and fictional referral wording", "Heading2")
    paragraph("This fictional final response records the demo review outcome. In a real case, the firm would confirm any payment arrangements and the applicable Financial Ombudsman Service referral rights, time limits and contact details before issue. This demonstration does not provide real referral instructions or determine real compensation.")
    paragraph("All figures and case details are fictional. Human approval here is a demonstration control only; this PDF is not legal advice or a real customer communication.")
    SimpleDocTemplate(stream, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                      topMargin=18*mm, bottomMargin=18*mm).build(story)
    return stream.getvalue()
