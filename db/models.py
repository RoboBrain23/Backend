from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    Time,
    Date,
    Table,
    Identity,
    Boolean,
    Numeric,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


# this table is a "junction table" to link between two tables (patient,caregiver)
association_table = Table(
    "association",  # Table Name
    Base.metadata,
    Column(
        "patient",
        ForeignKey("patient.id"),
    ),
    Column("caregiver", ForeignKey("caregiver.id")),
)
# # this table is a "junction table" to link between two tables (chair,caregiver)
# linking_table = Table(
#     "linking",  # Table Name
#     Base.metadata,
#     Column(
#         "chair", ForeignKey("chair.id"), Column("caregiver", ForeignKey("caregiver.id"))
#     ),
# )


class Chair(Base):
    __tablename__ = "chair"

    id = Column(Integer, primary_key=True, index=True)
    parcode = Column(Integer, unique=True, index=True)
    password = Column(String, nullable=False)
    available = Column(Boolean)

    # ? relationship with sensor_data
    sensor_data = relationship("SensorData", back_populates="chair")
    location = relationship("Location", uselist=False, back_populates="chair")

    def __str__(self):
        return f'"id": {self.id}, "password": {self.password}'


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Numeric(precision=9, scale=6))
    longitude = Column(Numeric(precision=9, scale=6))

    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", back_populates="location", cascade="delete")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    pulse_rate = Column(Float, nullable=False)
    oximeter = Column(Float, nullable=False)
    created_date = Column(Date, default=func.current_date())
    created_time = Column(Time, server_default=func.current_time())

    # ? relationship with chair
    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", back_populates="sensor_data")


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    gender = Column(String(length=5))
    age = Column(Integer)

    # ? one-to-one relationship with chair
    chair_id = Column(Integer, ForeignKey("chair.id"), index=True)
    chair = relationship("Chair", uselist=False, backref="patient")
    caregivers = relationship(
        "CareGiver", secondary=association_table, back_populates="patients"
    )


# TODO: Create Caregiver table with many-to-many relationship with patient table
class CareGiver(Base):
    __tablename__ = "caregiver"

    id = Column(
        Integer,
        Identity(start=1, increment=1, cycle=True, minvalue=1),
        primary_key=True,
        index=True,
    )
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    username = Column(String(length=150))
    email = Column(String(length=150))
    password = Column(String)
    age = Column(Integer)
    patients = relationship(
        "Patient", secondary=association_table, back_populates="caregivers"
    )
    # caregiverphone_id = Column(
    #     Integer,
    #     ForeignKey("caregiverphone.id"),
    #     index=True,
    # )
    # caregiverphone = relationship(
    #     "CareGiverPhone", back_populates="caregiver", foreign_keys=[caregiverphone_id]
    # )
    phones = relationship("CareGiverPhone", back_populates="caregiver")

    def __str__(self):
        return f"Care Giver : {self.first_name}"


class CareGiverPhone(Base):
    __tablename__ = "caregiverphone"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(length=25))
    caregiver_id = Column(
        Integer, ForeignKey("caregiver.id"), index=True, nullable=False
    )
    caregiver = relationship(
        "CareGiver", back_populates="phones", remote_side=[CareGiver.id], cascade="delete"
    )
