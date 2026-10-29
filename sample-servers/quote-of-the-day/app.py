from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

QUOTES = {
    "inspiration": [
        ("The best way out is always through.", "Robert Frost"),
        ("What we do now echoes in eternity.", "Marcus Aurelius"),
        ("Attention is the rarest and purest form of generosity.", "Simone Weil"),
    ],
    "humor": [
        ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison"),
        ("The trouble with having an open mind is that people insist on coming along and trying to put things in it.", "Terry Pratchett"),
        ("Everything is funny, as long as it's happening to somebody else.", "Will Rogers"),
    ],
    "engineering": [
        ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
        ("Premature optimization is the root of all evil.", "Donald Knuth"),
        ("Make it work, make it right, make it fast.", "Kent Beck"),
    ],
}


class QuoteRequest(BaseModel):
    category: str | None = None
    date: str | None = None


@app.post("/score")
async def quote_of_the_day(payload: QuoteRequest):
    """Returns a deterministic quote for a given day, matching the MCP tool contract."""
    category = (payload.category or "inspiration").lower()
    if category not in QUOTES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid 'category' value. Expected one of: {', '.join(sorted(QUOTES))}.",
        )

    if payload.date:
        try:
            day = date.fromisoformat(payload.date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid 'date' value. Expected YYYY-MM-DD.")
    else:
        day = date.today()

    # Indexing by ordinal keeps the same day returning the same quote.
    choices = QUOTES[category]
    quote, author = choices[day.toordinal() % len(choices)]
    return {
        "quote": quote,
        "author": author,
        "category": category,
        "date": day.isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
