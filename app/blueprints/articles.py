# 3rd party imports
from flask import Blueprint, request, jsonify

# Project imports
from app.models import Article

blp = Blueprint("articles", __name__)


@blp.route("/articles", methods=["GET"])
def get_articles():
    """
    Get articles endpoint.
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    articles = Article.get(page, per_page)
    articles = [article.to_dict() for article in articles]
    return jsonify({"data": articles})
