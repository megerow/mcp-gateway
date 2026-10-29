from datetime import date

from fastmcp import FastMCP

# The name given here is what the gateway reports back to clients as
# io.modelcontextprotocol/serverInfo, so pick something identifiable.
app = FastMCP("Quote Server")

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


def pick(category: str, day: date) -> tuple[str, str]:
    # Indexing by ordinal keeps the same day returning the same quote.
    choices = QUOTES[category]
    return choices[day.toordinal() % len(choices)]


@app.tool()
def quote_of_the_day(category: str = "inspiration", day: str | None = None) -> dict:
    """Returns the quote of the day. Categories: inspiration, humor, engineering.

    Pass day as YYYY-MM-DD for a specific date, otherwise today is used.
    """
    category = category.lower()
    if category not in QUOTES:
        raise ValueError(f"Invalid category {category!r}. Expected one of: {', '.join(sorted(QUOTES))}.")

    try:
        on = date.fromisoformat(day) if day else date.today()
    except ValueError:
        raise ValueError(f"Invalid day {day!r}. Expected YYYY-MM-DD.")

    quote, author = pick(category, on)
    return {"quote": quote, "author": author, "category": category, "date": on.isoformat()}


@app.resource("quote://today")
def today_quote() -> str:
    """Today's inspirational quote, for clients that read resources."""
    quote, author = pick("inspiration", date.today())
    return f"{quote} — {author}"


@app.prompt()
def reflect_on_quote(category: str = "engineering") -> str:
    """Ask the model to reflect on today's quote from a category."""
    quote, author = pick(category, date.today())
    return f'Reflect briefly on this quote and how it applies to my work today:\n\n"{quote}" — {author}'
