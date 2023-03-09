from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    chair_data = relationship("ChairData", back_populates="patient")


class ChairData(Base):
    __tablename__ = "chair_data"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    body_temperature = Column(Float, nullable=False)
    oximeter = Column(Float, nullable=False)
    heart_rate = Column(Float, nullable=False)
    sugar_level = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient_id = Column(Integer, ForeignKey("patient.id"))
    patient = relationship("Patient", back_populates="chair_data")
