# Native imports
import json

# 3rd party imports
from sqlalchemy import text
from flask import Blueprint, request, jsonify

# Project imports
from app.config.db import get_db
from app.config import settings

blp = Blueprint("chats", __name__)


@blp.route("/chats", methods=["POST"])
def chat():
    """
    Generate a chat response.
    """
    data = request.get_json()
    query_text = data.get("query")
    date = data.get("date")

    db = next(get_db())

    # Fetch similar articles
    query = text(
        """
        SELECT contents, metadata->>'article_id' as id
        FROM article_embeddings
        WHERE metadata->>'published_at' = :date
        ORDER BY embedding <=> ai.ollama_embed('llama3.2', :query_text, host=>:host)
        LIMIT 6
        """
    )
    result = db.execute(
        query, {"query_text": query_text, "date": date, "host": settings.ollama_host}
    )

    # Fetch results
    rows = result.fetchall()

    if len(rows) == 0:
        return jsonify(
            {"answer": "No articles found based on your question.", "article_id": None}
        )

    # Merge results
    context_text = ""
    context_ids = []
    for row in rows:
        context_ids.append(int(row[1]))
        context_text += f"ID: {row[1]} Content: {row[0]}\n\n"

    # Generate response
    query = text(
        """
        SELECT ai.ollama_chat_complete(
            'llama3.2',
            jsonb_build_array(
                jsonb_build_object('role', 'system', 'content', 'You are a helpful assistant. Use only the context provided to answer the question and provide the article ID from which your answer has more relation with. Format your response in JSON format like this: {"answer": "Your answer here", "article_id": 123}'),
                jsonb_build_object('role', 'user', 'content', format('Context: %s\n\nUser Question: %s\n\nAssistant:', CAST(:context_text AS TEXT), CAST(:query_text AS TEXT)))
            ),
            host=>:host
        )->'message'->>'content' as response;
        """
    )
    result = db.execute(
        query,
        {
            "query_text": query_text,
            "context_text": context_text,
            "host": settings.ollama_host,
        },
    )

    # Fetch response
    response = result.scalar()

    return jsonify(json.loads(response))
