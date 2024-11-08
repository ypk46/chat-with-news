# 3rd party imports
from flask import Blueprint, jsonify

# Project imports
from app.models import Article

blp = Blueprint("articles", __name__)


@blp.route("/articles", methods=["GET"])
def get_articles():
    """
    Get articles endpoint.
    """
    articles = Article.get_all()
    articles = [article.to_dict() for article in articles]
    return jsonify({"data": articles})
