import databases
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./pizza.sqlite"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
