# Native imports
import json
from datetime import datetime
from email.utils import parsedate_to_datetime

# 3rd party imports
import ollama
import newspaper


def get_article_date(entry: dict):
    """
    Extract and parse the publication date from a feedparser entry.

    Args:
        entry: A feedparser entry object

    Returns:
        datetime: The parsed publication date, or None if parsing fails
    """
    # Try different possible date fields
    for date_field in ["published", "updated", "created"]:
        date_str = entry.get(date_field)
        if date_str:
            try:
                # Try parsing RFC 2822 date format (common in RSS)
                return parsedate_to_datetime(date_str)
            except (TypeError, ValueError):
                try:
                    # Try parsing common ISO format
                    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except ValueError:
                    continue

    return None


def generate_summary(link: str):
    """
    Generate a summary for a given article link.

    Args:
        link (str): The URL of the article.
    """
    article = newspaper.Article(link)
    article.download()
    article.parse()

    # Generate prompt
    prompt = f"""
    Generate a summary of at 120 words and a list of tags/keywords
    for this article. Respond using JSON with the following structure:

    {{
        "summary": "...",
        "tags": [...],
    }}

    {article.text}
    """

    # Get the summary
    response = ollama.generate(model="llama3.2", prompt=prompt, format="json")
    response_str = response.get("response")

    # Parse to JSON
    response_json = json.loads(response_str)
    return {"content": article.text, **response_json}
