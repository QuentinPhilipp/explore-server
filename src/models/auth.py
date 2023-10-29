from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class LoginDetailsModel(Base):
    __tablename__ = "login_details"

    id = Column(BigInteger, primary_key=True, index=True)
    expires_at = Column(BigInteger)
    refresh_token = Column(String)
    access_token = Column(String)
    athlete_id = Column(BigInteger, ForeignKey('athletes.id'))
    athlete = relationship("AthleteModel")
