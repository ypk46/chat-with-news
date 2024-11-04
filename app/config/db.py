# 3rd party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Project imports
from app.config.settings import settings

# Create a database engine
engine = create_engine(settings.db_conn)

# Create a session maker
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create a Base class for declarative models
Base = declarative_base()
