from sqlalchemy import Column, BigInteger, String, DateTime, Float

from database.db import Base


class AthleteModel(Base):
    __tablename__ = "athletes"

    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    bio = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    sex = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    profile_medium = Column(String)
    weight = Column(Float)
