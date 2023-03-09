from sqlalchemy import Column, String, Integer, Float, ForeignKey, Time, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Chair(Base):
    __tablename__ = "chair"

    id = Column(Integer, primary_key=True)
    password = Column(String)

    # ? relationship with sensor_data
    sensor_data = relationship("SensorData", back_populates="chair")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)
    body_temperature = Column(Float)
    heart_rate = Column(Float)
    oximeter = Column(Float)
    sugar_level = Column(Float)
    created_date = Column(Date, default=func.current_date())
    created_time = Column(Time, server_default=func.current_time())

    # ? relationship with chair
    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", back_populates="sensor_date")


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    age = Column(String)

    # ? one to one relationship with chair
    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", uselist=False, back_populates="patient")


# TODO: Create Caregiver table with many to many relationship with patient table
