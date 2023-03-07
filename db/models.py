from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    patient_full_name = Column(String, nullable=False, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    password = Column(Text)
    address = Column(String)
    age = Column(Integer)
    gender = Column(String)

    chair_data = relationship("ChairData", back_populates="patient")


class ChairData(Base):
    __tablename__ = "chair_data"

    id = Column(Integer, primary_key=True, index=True)
    body_temperature = Column(Float, nullable=False)
    oximeter = Column(Float, nullable=False)
    heart_rate = Column(Float, nullable=False)
    sugar_level = Column(Float, nullable=False)

    patient_id = Column(Integer, ForeignKey("patient.id"))
    patient = relationship("Patient", back_populates="chair_data")
