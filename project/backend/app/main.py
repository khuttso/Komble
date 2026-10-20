"""Loopback development API for the shared application foundation."""

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse

from .content import PACKS
from .schemas import Pack
from .feedback import AnswerRequest, assess
from .extraction import extract
from .grounding import GuidanceRequest, answer
from .llm import ModelError


app = FastAPI(title="InterviewCoach", version="0.2.0", description="Local interview practice, job-advert extraction and grounded preparation guidance.")


@app.middleware("http")
async def response_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "InterviewCoach", "stage": "local-prototype"}


@app.get("/api/packs", response_model=list[Pack])
def list_packs():
    return PACKS


@app.exception_handler(ModelError)
async def model_error(request: Request, error: ModelError):
    return JSONResponse(status_code=error.status, content={"error": str(error)})


@app.post("/api/feedback")
def feedback(request: AnswerRequest):
    return assess(request)


@app.post("/api/extract")
def extraction(image: UploadFile):
    # Read at most limit+1 rather than materialising an arbitrarily large file.
    return extract(image.file.read(2 * 1024 * 1024 + 1))


@app.post("/api/guidance")
def guidance(request: GuidanceRequest):
    question = request.question.strip()
    if len(question) < 3:
        return JSONResponse(status_code=400, content={"error": "Enter a preparation question with at least three characters."})
    return answer(question)
