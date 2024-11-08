# Native imports
import json

# 3rd party imports
from sqlalchemy import text
from flask import Blueprint, request, jsonify

# Project imports
from app.config.db import get_db

blp = Blueprint("chats", __name__)


@blp.route("/chats", methods=["POST"])
def chat():
    """
    Generate a chat response.
    """
    data = request.get_json()
    query_text = data.get("query")

    db = next(get_db())

    # Fetch similar articles
    query = text(
        """
        SELECT contents, metadata->>'article_id' as id
        FROM article_embeddings
        ORDER BY embedding <=> ai.ollama_embed('llama3.2', :query_text, host=>'http://host.docker.internal:11434')
        LIMIT 3
        """
    )
    result = db.execute(query, {"query_text": query_text})

    # Fetch results
    rows = result.fetchall()

    # Merge results
    context_text = ""
    for row in rows:
        context_text += f"ID: {row[1]} Content: {row[0]}\n\n"

    # Generate response
    query = text(
        """
        SELECT ai.ollama_chat_complete(
            'llama3.2',
            jsonb_build_array(
                jsonb_build_object('role', 'system', 'content', 'You are a helpful assistant. Use only the context provided to answer the question and provide a JSON response like: {"answer": "The answer to the question.", "article_id": 123}'),
                jsonb_build_object('role', 'user', 'content', format('Context: %s\n\nUser Question: %s\n\nAssistant:', CAST(:context_text AS TEXT), CAST(:query_text AS TEXT)))
            ),
            host=>'http://host.docker.internal:11434'
        )->'message'->>'content' as response;
        """
    )
    result = db.execute(query, {"query_text": query_text, "context_text": context_text})

    # Fetch response
    response = result.scalar()

    return jsonify({"response": json.loads(response)})
