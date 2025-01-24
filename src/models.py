from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Database model representing platform users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    skills = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to service requests
    service_requests = relationship("ServiceRequest", back_populates="requester")

# Database model for service requests
class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    requester_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to user who made the request
    requester = relationship("User", back_populates="service_requests")