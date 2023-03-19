from sqlalchemy import Column, String, Integer, Float, ForeignKey, Time, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base
import uuid

association_table = Table(
    "association",  # Table Name
    Base.metadata,
    Column(
        "patient",
        ForeignKey("patient.id"),
    ),
    Column("caregiver", ForeignKey("caregiver.id")),
)


class Chair(Base):
    __tablename__ = "chair"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String)

    # ? relationship with sensor_data
    sensor_data = relationship("SensorData", back_populates="chair")

    def __str__(self):
        return f'"id": {self.id}, "password": {self.password}'


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    body_temperature = Column(Float)
    heart_rate = Column(Float)
    oximeter = Column(Float)
    sugar_level = Column(Float)
    created_date = Column(Date, default=func.current_date())
    created_time = Column(Time, server_default=func.current_time())

    # ? relationship with chair
    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", back_populates="sensor_data")


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    age = Column(String)

    # ? one-to-one relationship with chair
    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", uselist=False, backref="patient")
    caregivers = relationship(
        "CareGiver", secondary=association_table, back_populates="patients"
    )


# TODO: Create Caregiver table with many-to-many relationship with patient table
class CareGiver(Base):
    __tablename__ = "caregiver"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()), index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    age = Column(Integer)
    patients = relationship(
        "Patient", secondary=association_table, back_populates="caregivers"
    )
    # caregiverphone_id = Column(Integer, ForeignKey("caregiverphone.id"), index=True)
    # caregiverphone = relationship("CareGiverPhone", back_populates="caregiver")

    def __str__(self):
        return f"Care Giver : {self.first_name}"


# class CareGiverPhone(Base):
#     __tablename__ = "caregiverphone"
#     id = Column(Integer, primary_key=True, index=True)
#     phone_number = Column(String)
#     caregiver_id = Column(Integer, ForeignKey("caregiver.id"), index=True)
#     caregiver = relationship("CareGiver", back_populates="caregiverphone")


# class Associatian(Base):
#     __tablename__ = "care_giver_patient"

#     caregiver_id = Column(Integer, ForeignKey("care_giver.id"), primary_key=True)
#     patient_id = Column(Integer, ForeignKey("patient.id"), primary_key=True)

#     caregiver = relationship("CareGiver", back_populates="patient_id")
#     patient = relationship("Patient", back_populates="caregiver_id")
