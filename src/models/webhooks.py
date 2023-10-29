from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from database.db import Base


class WebhookActivitiesModel(Base):
    __tablename__ = "webhooks"

    id = Column(BigInteger, primary_key=True, index=True)
    object_type = Column(String)
    object_id = Column(BigInteger)
    aspect_type = Column(String)
    updates = Column(MutableDict.as_mutable(JSONB))  # noqa
    owner_id = Column(BigInteger, ForeignKey('athletes.id'))
    subscription_id = Column(BigInteger)
    event_time = Column(BigInteger)
