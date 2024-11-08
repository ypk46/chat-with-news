# Native imports
from datetime import datetime

# 3rd party imports
from flask import Blueprint, jsonify, request

# Project imports
from app.models import Article

blp = Blueprint("articles", __name__)


@blp.route("/articles", methods=["GET"])
def get_articles():
    """
    Get articles endpoint.
    """
    date = request.args.get("date")

    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except Exception:
        date = None

    if not date:
        date = datetime.now()

    articles = Article.get_by_date(date)
    articles = [article.to_dict() for article in articles]
    return jsonify({"data": articles})
