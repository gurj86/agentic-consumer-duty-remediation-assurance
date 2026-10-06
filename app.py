import os
import time
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from agent_workflow import run_assurance


app = FastAPI(title="Agentic Consumer Duty & Remediation Assurance")

MAX_FIELD_CHARS = 4000
RATE_LIMIT = 5
RATE_WINDOW_SECONDS = 3600
_requests_by_ip: dict[str, deque[float]] = defaultdict(deque)


class CaseInput(BaseModel):
    customer_circumstances: str
    interaction_notes: str
    vulnerability_support_needs: str
    actions_taken: str
    agent_rationale: str


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _check_rate_limit(request: Request) -> None:
    now = time.time()
    ip = _client_ip(request)
    bucket = _requests_by_ip[ip]

    while bucket and now - bucket[0] > RATE_WINDOW_SECONDS:
        bucket.popleft()

    if len(bucket) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Demo limit reached for this hour. Please try again later.",
        )

    bucket.append(now)


def _validate_demo_input(case: CaseInput) -> None:
    for field_name, value in case.model_dump().items():
        if len(value) > MAX_FIELD_CHARS:
            raise HTTPException(
                status_code=400,
                detail=f"{field_name} is too long for this portfolio demo.",
            )


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health():
    return {"status": "ok", "agentic_mode": bool(os.getenv("OPENAI_API_KEY"))}


@app.post("/api/review")
async def review_case(case: CaseInput, request: Request):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not set. Add it as an environment variable to run the live agentic workflow.",
        )

    _check_rate_limit(request)
    _validate_demo_input(case)

    try:
        result = await run_assurance(case.model_dump())
        return result.model_dump()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agentic review failed: {exc}") from exc
