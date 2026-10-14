"""Deterministic client letter and completion gate for the fictional demo."""
import io
import re
from decimal import Decimal
from datetime import datetime, timezone
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def amount(value):
    if not re.fullmatch(r"£?\s*(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d{2})?", str(value).strip()):
        raise ValueError("Redress must contain completed GBP amounts only.")
    return Decimal(str(value).replace("£", "").replace(",", "").strip())


def require_complete(result):
    outcome = result.get("recommendation")
    expected = {"Uphold": "Draft FRL - upheld", "Reject": "Draft FRL - not upheld"}
    if outcome not in expected or result.get("final_response_status") != expected[outcome]:
        raise ValueError("A final response requires a completed Uphold or Reject outcome.")
    if result.get("missing_evidence") or any(x.get("status") != "Confirmed" for x in result.get("evidence_matrix", [])):
        raise ValueError("Resolve outstanding evidence before approving a final response.")
    if not result.get("evidence_matrix") or not str(result.get("rationale", "")).strip():
        raise ValueError("Evidence and reasons are required for a final response.")
    if outcome == "Uphold":
        if result.get("redress_status") != "Calculated" or result.get("redress_trigger") != "Illustrative calculation permitted" or not result.get("redress_methodology_summary"):
            raise ValueError("Complete the fictional redress calculation before approval.")
        principal, interest, total = [amount(result.get(k, "")) for k in ("redress_principal", "redress_interest", "redress_total")]
        if principal + interest != total:
            raise ValueError("The fictional redress breakdown must reconcile to the total.")
    elif result.get("redress_status") != "Not applicable":
        raise ValueError("A not-upheld outcome must have no applicable redress.")


def build_final_response(result, reference, approved_at):
    require_complete(result)
    out = io.BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="LetterBody", fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=9, textColor=colors.HexColor("#24334a")))
    styles["Title"].textColor = colors.HexColor("#16365b")
    styles["Heading2"].textColor = colors.HexColor("#16365b")
    p = lambda text: Paragraph(escape(str(text)).replace("\n", "<br/>"), styles["LetterBody"])
    story = [Paragraph("Final Response Letter", styles["Title"]), p("FICTIONAL PORTFOLIO DEMONSTRATION - NOT A REGULATED COMMUNICATION"), p(f"Complaint reference: {reference}\nDate: {datetime.fromtimestamp(approved_at, timezone.utc):%d %B %Y}\nHuman reviewer approval recorded (demo)"), p("Dear Customer,"), p("Thank you for giving us the opportunity to review your fictional motor finance complaint. This letter sets out the completed outcome approved by the human reviewer in this portfolio demonstration.")]
    def section(title, text):
        story.extend([Paragraph(title, styles["Heading2"]), p(text)])
    section("Complaint outcome", "Your complaint is upheld." if result["recommendation"] == "Uphold" else "Your complaint is not upheld. No fictional redress is payable (£0.00).")
    section("Your complaint", result.get("complaint_summary", ""))
    story.append(Paragraph("Evidence considered", styles["Heading2"]))
    for evidence in result["evidence_matrix"]:
        story.append(p(f"{evidence.get('item', '')}: {evidence.get('observation', '')} (Source: {evidence.get('source', '')})"))
    section("Reasons for our decision", result["rationale"])
    story.append(Paragraph("Fictional redress", styles["Heading2"]))
    upheld = result["recommendation"] == "Uphold"
    gbp = lambda key: f"£{amount(result[key]):,.2f}" if upheld else "£0.00"
    table = Table([[p("Component"), p("Fictional amount")], [p("Interest overpayment"), p(gbp("redress_principal"))], [p("Compensatory interest"), p(gbp("redress_interest"))], [p("Total fictional redress"), p(gbp("redress_total"))]], colWidths=[110*mm, 55*mm])
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), colors.HexColor("#edf2f7")), ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#edf2f7")), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 10), ("TOPPADDING", (0,0), (-1,-1), 8), ("LINEBELOW", (0,0), (-1,-1), .4, colors.HexColor("#ccd5df"))]))
    story.extend([table, Spacer(1, 10)])
    section("Calculation basis", result["redress_methodology_summary"] if upheld else "The completed evidence review does not support upholding your complaint under the supplied fictional methodology. No overpayment refund or compensatory interest is awarded.")
    section("Next steps", "Review the outcome and fictional calculation above. In this demonstration, the case can proceed to simulated settlement and closure after approval. No payment will be made and no action is required from a real customer." if upheld else "Review the reasons and evidence above. In this demonstration, the approved case can proceed to closure with £0.00 redress. No real customer action is required.")
    section("Financial Ombudsman Service - demonstration wording", "For illustration only: if you remain dissatisfied with a firm's final response, you may have the right to refer your complaint to the Financial Ombudsman Service free of charge, normally within six months of the date of the final response. Applicable eligibility, time limits and any complaint-specific rules would need to be verified for a real case. This fictional letter does not start a referral deadline, confer referral rights or constitute an actual final response. Do not submit this demonstration letter to the Financial Ombudsman Service.")
    story.extend([p("Yours sincerely,\nFictional Complaints Review Team"), p("All case information, methodology and redress figures are fictional portfolio data. This document is not issued by a regulated firm and must not be used as legal, regulatory or financial advice.")])
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#61708a"))
        canvas.drawString(22*mm, 14*mm, "FICTIONAL DEMO | Not a regulated customer communication")
        canvas.drawRightString(188*mm, 14*mm, f"Page {doc.page}")
    SimpleDocTemplate(out, pagesize=A4, rightMargin=22*mm, leftMargin=22*mm, topMargin=20*mm, bottomMargin=24*mm, title="Fictional Final Response Letter", author="Portfolio Demonstration").build(story, onFirstPage=footer, onLaterPages=footer)
    return out.getvalue()
