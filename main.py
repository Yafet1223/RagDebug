from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from db import SessionLocal, init_db
from rag import get_debug_answer

app = FastAPI(title="RAG Debug Mentor")

BASE_DIR = Path(__file__).resolve().parent
init_db()


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/styles.css")
def styles():
    return FileResponse(BASE_DIR / "static" / "styles.css")


@app.get("/health")
def health():
    return JSONResponse({"status": "ok"})


@app.post("/debug")
def debug_error(req: QueryRequest):
    answer = get_debug_answer(req.query)

    if SessionLocal is not None:
        try:
            db = SessionLocal()
            from db import DebugLog

            log = DebugLog(query=req.query, answer=answer)
            db.add(log)
            db.commit()
            db.close()
        except Exception as exc:  # pragma: no cover - depends on DB availability
            print(f"Log save skipped: {exc}")

    return {"query": req.query, "answer": answer}
