import base64
import hashlib
import hmac
import io
import json
import re
import secrets
import time
from decimal import Decimal
from html import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

# Ephemeral signing key: approvals expire and are invalidated on service restart.
_KEY = secrets.token_bytes(32)
WARNING = 'Fictional portfolio demonstration only. No payment is authorised. This is not current FCA scheme methodology.'


def seal(data):
    payload = base64.urlsafe_b64encode(json.dumps({'expires': time.time() + 3600, **data}).encode()).decode()
    signature = hmac.new(_KEY, payload.encode(), hashlib.sha256).hexdigest()
    return payload + '.' + signature


def unseal(token):
    try:
        payload, signature = token.split('.')
        if not hmac.compare_digest(signature, hmac.new(_KEY, payload.encode(), hashlib.sha256).hexdigest()):
            raise ValueError()
        data = json.loads(base64.urlsafe_b64decode(payload))
        if data['expires'] < time.time():
            raise ValueError()
        return data
    except Exception as exc:
        raise ValueError('This review has expired or is invalid. Run the workflow again.') from exc


def money(value):
    return f'£{Decimal(value):,.2f}'


def prepare(result, case):
    data = result.model_dump() if hasattr(result, 'model_dump') else dict(result)
    outcome = data['recommendation']
    data.update(final_response_draft='', review_token='', redress_breakdown=None)
    if outcome not in ('Uphold', 'Reject') or data.get('missing_evidence'):
        data.update(final_response_status='Not generated - investigation incomplete', redress_principal='', redress_interest='', redress_total='')
        return data
    breakdown = {'actual_rate': 'Not applicable', 'comparator_rate': 'Not applicable', 'principal': '£0.00', 'interest': '£0.00', 'total': '£0.00', 'basis': 'Complaint not upheld; no redress payable in this fictional case.'}
    if outcome == 'Uphold':
        inputs = case.get('illustrative_redress_inputs', '')
        rates = re.search(r'actual flat rate ([\d.]+)%; fictional comparator flat rate ([\d.]+)%', inputs)
        amounts = re.findall(r'£([\d,]+\.\d{2})', inputs)
        if not rates or len(amounts) != 3 or data.get('redress_status') != 'Calculated':
            data.update(final_response_status='Not generated - completed fictional calculation required', redress_status='Pending human approval', redress_principal='', redress_interest='', redress_total='')
            return data
        principal, interest, total = [Decimal(x.replace(',', '')) for x in amounts]
        if principal < 0 or interest < 0 or principal + interest != total:
            data.update(final_response_status='Not generated - calculation does not reconcile', redress_status='Pending human approval', redress_principal='', redress_interest='', redress_total='')
            return data
        breakdown.update(actual_rate=rates[1] + '% flat', comparator_rate=rates[2] + '% flat', principal=money(principal), interest=money(interest), total=money(total), basis='Supplied reconciled payment schedule: actual-rate payments less fictional comparator-rate payments. Supplied 8% simple compensatory interest on each overpayment to the fictional settlement date. The comparator and interest basis require human review; figures are pre-calculated, not inferred from the headline rates.')
    data.update(redress_breakdown=breakdown, redress_principal=breakdown['principal'], redress_interest=breakdown['interest'], redress_total=breakdown['total'], redress_methodology_summary=breakdown['basis'])
    upheld = outcome == 'Uphold'
    letter = '\n\n'.join(['FICTIONAL DEMO — FINAL RESPONSE', 'Dear customer,', 'Your motor finance commission complaint', 'We have completed our investigation. We ' + ('uphold your complaint.' if upheld else 'do not uphold your complaint.'), 'Evidence considered: ' + '; '.join(x.get('item', '') + ' (' + x.get('status', '') + ')' for x in data.get('evidence_matrix', [])), 'Our reasons: ' + data.get('rationale', ''), ('To put things right in this fictional example, the completed redress is:' if upheld else 'No redress is payable in this fictional example.') + '\nPrincipal overpayment: ' + breakdown['principal'] + '\nCompensatory interest: ' + breakdown['interest'] + '\nTotal: ' + breakdown['total'], 'Calculation basis: ' + breakdown['actual_rate'] + ' actual rate; ' + breakdown['comparator_rate'] + ' comparator rate. ' + breakdown['basis'], 'If you remain dissatisfied, a real final response would explain the applicable Financial Ombudsman Service referral rights and time limits, verified by the human reviewer. This fictional letter does not start a referral deadline.', 'Yours sincerely,\nFictional Complaints Team', WARNING])
    data.update(final_response_draft=letter, final_response_status='Draft FRL - awaiting human approval')
    data['review_token'] = seal({'approved': False, 'outcome': outcome, 'letter': letter, 'breakdown': breakdown})
    return data


def approve(token, reviewer):
    data = unseal(token)
    if data.get('outcome') not in ('Uphold', 'Reject') or not reviewer.strip():
        raise ValueError('A completed outcome and named human reviewer are required.')
    data.update(approved=True, reviewer=reviewer.strip()[:120], approved_at=time.strftime('%d %B %Y %H:%M UTC', time.gmtime()))
    return seal(data)


def pdf(token):
    data = unseal(token)
    if not data.get('approved'):
        raise ValueError('Human approval is required before downloading the final response.')
    stream = io.BytesIO()
    styles = getSampleStyleSheet()
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 13
    story = [Paragraph('Final response', styles['Title']), Paragraph('FICTIONAL MOTOR FINANCE COMPLAINT', styles['Heading2']), Paragraph(escape(WARNING), styles['Normal']), Spacer(1, 6*mm)]
    rows = [['Fictional redress breakdown', 'Amount']] + [[label, data['breakdown'][key]] for label, key in [('Principal overpayment', 'principal'), ('Compensatory interest', 'interest'), ('Total fictional redress', 'total')]]
    table = Table(rows, colWidths=[115*mm, 55*mm])
    table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0b1736')), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#eef3ff')), ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'), ('ALIGN', (1,0), (1,-1), 'RIGHT'), ('TOPPADDING', (0,0), (-1,-1), 9), ('BOTTOMPADDING', (0,0), (-1,-1), 9)]))
    story += [table, Spacer(1, 6*mm)]
    for section in data['letter'].split('\n\n')[1:]:
        story += [Paragraph(escape(section).replace('\n', '<br/>'), styles['Normal']), Spacer(1, 3*mm)]
    story += [KeepTogether([Paragraph('Human approval', styles['Heading2']), Paragraph(escape(data['reviewer'] + ' · ' + data['approved_at']) + '<br/>Approved for demonstration issue only.', styles['Normal'])])]
    def footer(canvas, doc):
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#667085'))
        canvas.drawString(20*mm, 14*mm, 'Fictional data only · Portfolio demonstration')
        canvas.drawRightString(190*mm, 14*mm, f'Page {doc.page}')
    SimpleDocTemplate(stream, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=24*mm, title='Fictional final response').build(story, onFirstPage=footer, onLaterPages=footer)
    return stream.getvalue()
