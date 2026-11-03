import asyncio
import ast
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.testclient import TestClient
from pydantic import ValidationError
import vehicle_quality_workflow as workflow


class VehicleWorkflowTests(unittest.TestCase):
    def test_walkthrough_outcomes_and_source_traceability(self):
        complete = workflow.walkthrough("complete")
        self.assertEqual(complete["recommendation"], "Uphold")
        self.assertTrue(complete["redress_ready"])
        self.assertIn("£655", complete["redress_explanation"])
        self.assertEqual(complete["tools_executed"], [])
        self.assertTrue(all(step["evidence_source"] for step in complete["steps"]))
        gap = workflow.walkthrough("gap")
        self.assertEqual(gap["recommendation"], "Further Investigation")
        self.assertFalse(gap["redress_ready"])
        self.assertEqual(gap["final_response_draft"], "")
        self.assertTrue(gap["missing_evidence"])

    def test_input_validation(self):
        for updates in ({"complaint": ""}, {"evidence": "x" * 12001}, {"mode": "unknown"}):
            with self.assertRaises(ValidationError):
                workflow.ReviewRequest(**{**workflow.BASE_CASE, **updates})

    def test_live_result_blocks_incomplete_response_and_captures_actual_calls(self):
        fake_output = workflow.walkthrough("gap")
        fake_output.update(redress_ready=True, final_response_draft="Must be suppressed")
        result = workflow.VehicleResult(**fake_output)
        runner = SimpleNamespace(run=AsyncMock(return_value=SimpleNamespace(
            final_output=result, new_items=[SimpleNamespace(type="tool_call_item", raw_item={"name": "evidence_review"})])))
        class Agent:
            def __init__(self, **kwargs):
                self.kwargs = kwargs
            def as_tool(self, **kwargs):
                return kwargs
        with patch.dict(sys.modules, {"agents": SimpleNamespace(Agent=Agent, Runner=runner)}):
            actual = asyncio.run(workflow.run_vehicle_review(workflow.VehicleCase(**workflow.GAP_CASE)))
        self.assertFalse(actual["redress_ready"])
        self.assertEqual(actual["final_response_draft"], "")
        self.assertEqual(actual["tools_executed"], ["evidence_review"])
        self.assertEqual(actual["mode"], "live")

    def test_http_routes(self):
        # Compile the actual added route functions independently of unrelated
        # document libraries / existing portfolio modules.
        source = ast.parse(Path("app.py").read_text(encoding="utf-8"))
        names = {"vehicle_quality_page", "vehicle_quality_examples", "vehicle_quality_run", "_require_api_key"}
        module = ast.Module(body=[n for n in source.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in names], type_ignores=[])
        app = FastAPI()
        scope = {**vars(workflow), "app": app, "HTMLResponse": HTMLResponse, "Request": Request, "HTTPException": HTTPException, "Path": Path, "__file__": str(Path("app.py").resolve()), "os": os, "_check_rate_limit": lambda request: None}
        exec(compile(module, "app.py", "exec"), scope)
        client = TestClient(app)
        self.assertIn("Vehicle Quality", client.get("/vehicle-quality").text)
        examples = client.get("/api/vehicle-quality/examples").json()
        for scenario in ["complete", "gap"]:
            response = client.post("/api/vehicle-quality/run", json={**examples[scenario], "scenario": scenario})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["mode"], "walkthrough")
        self.assertEqual(client.post("/api/vehicle-quality/run", json={}).status_code, 422)
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            response = client.post("/api/vehicle-quality/run", json={**examples["complete"], "mode": "live"})
            self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()

