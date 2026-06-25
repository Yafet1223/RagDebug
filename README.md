# RAG Debug Mentor

A simple FastAPI app that helps you debug common programming errors using a lightweight RAG-style workflow over a local knowledge file.

## Features

- Clean web UI with HTML and CSS
- FastAPI backend for error analysis
- Local knowledge-based debugging suggestions from the bundled error database
- Optional logging to a database if configured

## Project Structure

- `main.py` - FastAPI app and routes
- `rag.py` - error matching and debugging response generation
- `db.py` - optional database logging setup
- `templates/` - HTML UI
- `static/` - CSS styles
- `error.txt` - sample debugging knowledge base

## Requirements

Install dependencies with:

```bash
pip install -r Requirments.txt
fastapi
uvicorn
```

## Run the app

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/
```

## API

### POST /debug

Send a JSON payload like this:

```json
{
  "query": "FastAPI 422 Validation Error"
}
```

The endpoint returns a helpful debugging suggestion based on the local knowledge base.

## Notes

- The current implementation uses the local error knowledge file and does not require a Google API key.
- Database logging is optional and will only work if PostgreSQL is available and configured.
