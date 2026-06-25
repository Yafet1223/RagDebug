from pathlib import Path

DATA_FILE = Path(__file__).with_name("error.txt")


def _load_entries():
    text = DATA_FILE.read_text(encoding="utf-8")
    entries = []
    current = {"title": "", "cause": "", "fix": ""}

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current["title"]:
                entries.append(current)
                current = {"title": "", "cause": "", "fix": ""}
            continue

        if stripped.startswith("ERROR:"):
            if current["title"]:
                entries.append(current)
            current = {"title": stripped.replace("ERROR:", "", 1).strip(), "cause": "", "fix": ""}
        elif stripped.startswith("CAUSE:"):
            current["cause"] = stripped.replace("CAUSE:", "", 1).strip()
        elif stripped.startswith("FIX:"):
            current["fix"] = stripped.replace("FIX:", "", 1).strip()

    if current["title"]:
        entries.append(current)

    return entries


def get_debug_answer(query: str) -> str:
    if not query or not query.strip():
        return "Please describe the error you are seeing so I can help you debug it."

    entries = _load_entries()
    q = query.lower()
    words = [word for word in q.replace("-", " ").split() if len(word) > 2]

    scored = []
    for entry in entries:
        haystack = f"{entry['title']} {entry['cause']} {entry['fix']}".lower()
        score = sum(2 for word in words if word in haystack)
        if score > 0:
            scored.append((score, entry))

    if scored:
        _, best = max(scored, key=lambda item: item[0])
        return (
            f"Likely match: {best['title']}\n\n"
            f"Cause: {best['cause']}\n"
            f"Fix: {best['fix']}\n\n"
            "Try sharing the full traceback if you want a more precise diagnosis."
        )

    return (
        "I could not find a direct match, but here is a helpful starting point:\n\n"
        "- Re-check the exact error message and traceback.\n"
        "- Confirm the request payload and required fields.\n"
        "- Search for the error text in your code and dependency logs."
    )