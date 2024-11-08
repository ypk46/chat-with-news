# Native imports
from datetime import timedelta

# 3rd party imports
import click
from timescale_vector import client, pgvectorizer
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores.timescalevector import TimescaleVector

# Project imports
from app.config import settings
from app.models import *  # pylint: disable=W0401, W0614


def get_document(article: dict):
    """
    Get LangChain Document instance from article instance.

    Args:
        article (dict): Article instance.

    Returns:
        List[Document]: List of Document instances.
    """
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    docs = []
    for chunk in text_splitter.split_text(article["content"]):
        content = f"Title: {article['title']}, Content:{chunk}"
        metadata = {
            "id": str(client.uuid_from_time(article["published_at"])),
            "article_id": article["id"],
            "tags": article["tags"],
            "published_at": article["published_at"].strftime("%Y-%m-%d"),
        }
        docs.append(Document(page_content=content, metadata=metadata))

    return docs


def embed_and_write(articles, vectorizer):
    """
    Embed the articles and write to the vector store.

    Args:
        articles (List[dict]): List of articles to embed.
        vectorizer (pgvectorizer.Vectorize): Vectorizer instance.

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

    # Delete old embeddings that are no longer needed. They are identified by the locked_id column
    metadata_for_delete = [{"article_id": article["locked_id"]} for article in articles]
    vector_store.delete_by_metadata(metadata_for_delete)

    # Generate Document instance for each article
    documents = []
    for article in articles:
        if article["id"]:
            documents.extend(get_document(article))

    if len(documents) == 0:
        return

    # Embed the documents and write to the vector store
    texts = [d.page_content for d in documents]
    metadatas = [d.metadata for d in documents]
    ids = [d.metadata["id"] for d in documents]
    vector_store.add_texts(texts, metadatas, ids)


@click.command("vectorize")
def cmd_vectorize() -> None:
    """
    Create vector embeddings from the news artcles
    table.
    """
    # Create work queue for the articles table (this method is idempotent)
    vectorizer = pgvectorizer.Vectorize(settings.db_conn_timescale, "articles")
    vectorizer.register()

    # Process embeddings based on the work queue
    while vectorizer.process(embed_and_write) > 0:
        pass
