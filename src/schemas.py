from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

# Base model for user-related operations
class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    skills: Optional[List[str]] = []

# Model for user creation
class UserCreate(UserBase):
    password: str =Field(min_length=8)

# Model for returning user information
class UserResponse(UserBase):
    id: int
    created_at: datetime

    # Enabling ORM
    model_config = ConfigDict(from_attributes=True)

# Base model for service requests
class ServiceRequestBase(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10)

# Model for creating service requests
class ServiceRequestCreate(ServiceRequestBase):
    requester_id: int

# Model for returning service request details
class ServiceRequestResponse(ServiceRequestBase):
    id: int
    requester_id: int
    status: str
    created_at: datetime

    # Enables ORM
    model_config = ConfigDict(from_attributes=True)