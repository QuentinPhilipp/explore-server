from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class ActivityModel(Base):
    __tablename__ = "activities"

    id = Column(BigInteger, primary_key=True, index=True)
    athlete_id = Column(BigInteger, ForeignKey('athletes.id'))
    athlete = relationship("AthleteModel")
    name = Column(String)
    distance = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    total_elevation_gain = Column(Float)
    elev_high = Column(Float)
    elev_low = Column(Float)
    sport_type = Column(String)
    start_date = Column(DateTime)
    start_date_local = Column(DateTime)
    timezone = Column(String)
    start_lat = Column(String)
    start_lng = Column(String)
    end_lat = Column(String)
    end_lng = Column(String)
    polyline = Column(String)
    trainer = Column(Boolean)
    commute = Column(Boolean)
    manual = Column(Boolean)
    private = Column(Boolean)
    visibility = Column(String)
    flagged = Column(Boolean)
    workout_type = Column(Integer)
    average_speed = Column(Float)
    max_speed = Column(Float)
    hide_from_home = Column(Boolean)
    gear_id = Column(String)
    average_watts = Column(Float)
    device_watts = Column(Boolean)
    max_watts = Column(Integer)
    weighted_average_watts = Column(Integer)
