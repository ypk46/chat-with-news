# 3rd party imports
import click
import waitress
from flask import Flask
from flask_cors import CORS

# Project imports
from app.config import Base, engine, settings
from app.models import *  # pylint: disable=W0401, W0614
from app.blueprints import *  # pylint: disable=W0401, W0614


@click.command("serve")
@click.option("--port", default=5000, help="Port to run the server on.")
@click.option("--threads", default=4, help="Number of threads to run the server on.")
def cmd_serve(port: int, threads: int) -> None:
    """
    Serve the ChatWithNews API.
    """
    Base.metadata.create_all(bind=engine)

    # Set up Flask app
    app = Flask(__name__)
    CORS(app)

    # Register blueprints
    app.register_blueprint(articles_blp, url_prefix="/api")
    app.register_blueprint(chats_blp, url_prefix="/api")

    # Run the app
    if settings.env == "dev":
        app.run(port=port, debug=True)

    else:
        waitress.serve(app, host="0.0.0.0", port=port, threads=threads)
