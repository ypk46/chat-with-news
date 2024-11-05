# Native imports
from datetime import timedelta

# 3rd party imports
import click
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.timescalevector import TimescaleVector

# Project imports
from app.config import settings


@click.command("search")
@click.option("--query", type=str, prompt="Search query")
def cmd_search(query: str) -> None:
    """
    Search for articles.

    Args:
        query (str): Search query.

    Returns:
        None
    """
    embedding = OllamaEmbeddings(model="llama3.2", base_url=settings.ollama_host)
    vector_store = TimescaleVector(
        collection_name="article_embeddings",
        service_url=settings.db_conn_timescale,
        embedding=embedding,
        num_dimensions=3072,
        time_partition_interval=timedelta(days=30),
    )

    results = vector_store.similarity_search_with_score(query, 5)
    print(results)
