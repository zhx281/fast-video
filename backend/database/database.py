from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Link to the sqlite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Linking the engine to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})

# Create local session with engine
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


# Calling the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
