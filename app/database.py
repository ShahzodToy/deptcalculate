from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:admin123@localhost/dept_db')

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base= declarative_base()