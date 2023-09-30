from sqlalchemy import Column, ForeignKey, String, Float, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from database.db import Base


class Athlete(Base):
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


class LoginDetails(Base):
    __tablename__ = "login_details"

    id = Column(BigInteger, primary_key=True, index=True)
    expires_at = Column(BigInteger)
    refresh_token = Column(String)
    access_token = Column(String)
    athlete_id = Column(BigInteger, ForeignKey('athletes.id'))
    athlete = relationship("Athlete")


class WebhookActivities(Base):
    __tablename__ = "webhooks"

    id = Column(BigInteger, primary_key=True, index=True)
    object_type = Column(String)
    object_id = Column(BigInteger)
    aspect_type = Column(String)
    updates = Column(MutableDict.as_mutable(JSONB))  # noqa
    owner_id = Column(BigInteger, ForeignKey('athletes.id'))
    subscription_id = Column(BigInteger)
    event_time = Column(BigInteger)
