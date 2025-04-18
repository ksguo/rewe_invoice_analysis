from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Add SSL parameters for production environments
import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}@"
    f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Create the SQLAlchemy engine with SSL for production
if os.environ.get("ENVIRONMENT") == "production":
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "sslmode": "require",
        },
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e  # Re-raise the exception so FastAPI can handle it
    finally:
        db.close()
