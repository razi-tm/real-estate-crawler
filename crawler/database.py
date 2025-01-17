from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "postgresql://user:password@postgres:5432/real_estate"
Base = declarative_base()

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    region = Column(String)
    trucheck = Column(Boolean)

def setup_database():
    """Setup the database and return a session maker."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

Session = setup_database()

def save_to_database(details):
    """Save listing details to the database."""
    try:
        print(f"##################Details received for saving: {details}")
        print(f"***Attempting to save: {details}")  # Debug log
        with Session() as session:
            listing = Listing(**details)
            session.add(listing)
            session.commit()
            print(f"Saved to database: {details}")
    except IntegrityError:
        print(f"Duplicate entry for URL: {details['url']}")
    except Exception as e:
        print(f"Error saving to database: {e}")
