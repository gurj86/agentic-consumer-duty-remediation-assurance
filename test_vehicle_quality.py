import ast
import asyncio
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.testclient import TestClient

def finish(coro):
    try:
        coro.send(None)
    except StopIteration as done:
        return done.value
    raise AssertionError('Unexpected IO in isolated test')

class FakeAgent:
    def __init__(self, **kwargs): self.kwargs = kwargs
    def as_tool(self, **kwargs): return kwargs

with patch.dict(sys.modules, {'agents': SimpleNamespace(Agent=FakeAgent, Runner=SimpleNamespace())}):
    import vehicle_quality_workflow as workflow

ROOT = Path(__file__).parent

def result(outcome='Uphold'):
    return workflow.ComplaintWorkflowResult(
        complaint_summary='Recurring fault', complaint_category='Vehicle quality',
        recommendation=outcome, rationale='Evidence supports review', methodology_check='Fictional methodology',
        redress_trigger='Illustrative calculation permitted', redress_status='Calculated',
        redress_principal='£655.00', redress_interest='£0.00', redress_total='£655.00',
        redress_methodology_summary='Supplied figures', final_response_status='Draft FRL - upheld',
        final_response_draft='Fictional draft', human_review_note='Approval required')

class VehicleTests(unittest.TestCase):
    def test_incomplete_gate(self):
        for outcome in ['Further Investigation', 'Escalate']:
            actual=workflow.enforce_incomplete_gate(result(outcome))
            self.assertEqual(actual.final_response_draft, '')
            self.assertEqual(actual.redress_total, '')
            self.assertEqual(actual.redress_trigger, 'Not reached')
        self.assertEqual(workflow.enforce_incomplete_gate(result()).redress_total, '£655.00')

    def test_actual_tools_and_schema(self):
        runner=SimpleNamespace(run=AsyncMock(return_value=SimpleNamespace(final_output=result(),new_items=[SimpleNamespace(type='tool_call_item',raw_item={'name':'review_vehicle_quality'})])))
        with patch.object(workflow,'Runner',runner):
            actual=finish(workflow.run_vehicle_review({'complaint_text':'Fictional'}))
        self.assertEqual(actual.agents_consulted,['Vehicle Quality & Repair Specialist'])
        self.assertEqual(actual.redress_total,'£655.00')
        self.assertEqual(workflow.lead.kwargs['output_type'], workflow.ComplaintWorkflowResult)

    def test_matching_page(self):
        import re
        vehicle=(ROOT/'vehicle_quality.html').read_text(encoding='utf-8')
        commission=(ROOT/'complaint_redress.html').read_text(encoding='utf-8')
        self.assertEqual(re.search(r'<style>(.*?)</style>',vehicle,re.S)[1],re.search(r'<style>(.*?)</style>',commission,re.S)[1])
        self.assertNotRegex(vehicle.lower(),r'interview|walkthrough|simulated fulfilment')
        self.assertIn('/api/vehicle-quality/final-response.pdf',vehicle)

    def test_routes_use_existing_controls(self):
        names={'vehicle_quality_page','vehicle_quality_extract','vehicle_quality_run','vehicle_quality_final_response','_require_api_key','_validate_demo_input'}
        source=ast.parse((ROOT/'app.py').read_text(encoding='utf-8'))
        module=ast.Module(body=[n for n in source.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names],type_ignores=[])
        app=FastAPI(); review=AsyncMock(return_value=result()); extract=AsyncMock(return_value={'files':[]})
        scope={**vars(workflow),'app':app,'Request':Request,'File':File,'UploadFile':UploadFile,'Response':Response,'HTMLResponse':HTMLResponse,'HTTPException':HTTPException,'Path':Path,'__file__':str(ROOT/'app.py'),'os':os,'MAX_FIELD_CHARS':12000,'MAX_EXTRACTED_CHARS_PER_FILE':18000,'MAX_UPLOAD_FILES':3,'_check_rate_limit':lambda request:None,'_extract_uploaded_files':extract,'run_vehicle_review':review,'build_final_response_pdf':lambda payload:b'%PDF-fixture'}
        exec(compile(module,'app.py','exec'),scope)
        case=workflow.VehicleQualityInput(**{k:'Fictional evidence' for k in workflow.VehicleQualityInput.model_fields})
        self.assertIn('Vehicle Quality',finish(scope['vehicle_quality_page']()))
        with patch.dict(os.environ,{'OPENAI_API_KEY':''}):
            with self.assertRaises(HTTPException) as error:
                finish(scope['vehicle_quality_run'](case,None))
            self.assertEqual(error.exception.status_code,503)
        with patch.dict(os.environ,{'OPENAI_API_KEY':'test-placeholder'}):
            self.assertEqual(finish(scope['vehicle_quality_run'](case,None))['redress_total'],'£655.00')
            case.complaint_text='x'*12001
            with self.assertRaises(HTTPException) as error:
                finish(scope['vehicle_quality_run'](case,None))
            self.assertEqual(error.exception.status_code,400)
        self.assertEqual(finish(scope['vehicle_quality_extract'](None,[])),{'files':[]})
        self.assertEqual(finish(scope['vehicle_quality_final_response']({})).media_type,'application/pdf')

if __name__=='__main__': unittest.main()

