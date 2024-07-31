from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Adjust the following PostgreSQL URL to match your database settings
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:samirsamir@localhost/sideProject"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Optional: Add any engine-specific arguments here
)

# Each instance of the SessionLocal class will be a database session
# The class itself is not a database session yet
SessionLocal = sessionmaker(
    autocommit=False,  # Do not commit automatically
    autoflush=False,   # Do not flush automatically
    bind=engine        # Bind the configuration to the engine
)

# Base class for our classes definitions
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()