# Native imports
import logging

# 3rd party imports
import click
import feedparser

# Project imports
from app.config import settings
from app.utils.feed import generate_summary, get_article_date
from app.models import *  # pylint: disable=W0401, W0614

logger = logging.getLogger(settings.name)


@click.group("feed")
def feed_group() -> None:
    """
    Feed commands.
    """


@feed_group.command("add")
@click.option("--name", type=str, prompt="Feed name")
@click.option("--url", type=str, prompt="RSS feed URL")
@click.option("--image", type=str, prompt="Feed image URL")
def cmd_feed_add(name: str, url: str, image: str) -> None:
    """
    Add a new RSS feed to the database.

    Args:
        name (str): Feed name.
        url (str): RSS feed URL.
        image (str): Feed image URL.

    Returns:
        None
    """
    feed = Feed.create({"name": name, "url": url, "image": image})
    click.echo(f"Feed added: {feed.name} ({feed.url})")


@feed_group.command("list")
def cmd_feed_list() -> None:
    """
    List all RSS feeds in the database.

    Returns:
        None
    """
    feeds = Feed.get_all()
    for feed in feeds:
        click.echo(f"{feed.name} ({feed.url})")


@feed_group.command("fetch")
def cmd_feed_fetch() -> None:
    """
    Fetch news from all RSS feeds.

    Returns:
        None
    """
    feeds = Feed.get_all()
    for feed in feeds:
        # Parse the feed
        parsed = feedparser.parse(feed.url)

        # Iterate over entries
        for entry in parsed.entries[:10]:
            try:
                # Get the publication date
                published_at = get_article_date(entry)

                # Check if summary is valid
                data = generate_summary(entry.link)

                if data is None:
                    click.echo(f"Skipping entry due to invalid summary: {entry.title}")

                if data.get("summary") is None:
                    click.echo(f"Skipping entry due to empty summary: {entry.title}")
                    continue

                # Insert the article into the database
                Article.create(
                    {
                        "title": entry.title,
                        "content": data.get("content"),
                        "summary": data.get("summary"),
                        "tags": data.get("tags"),
                        "link": entry.link,
                        "published_at": published_at,
                        "feed_image": feed.image,
                        "feed_name": feed.name,
                    }
                )

            except Exception:
                logger.exception("Failed to process article entry.")
