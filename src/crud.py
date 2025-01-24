from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import typing

from . import models, schemas

# Password hashing config
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    '''
    hash password with bcrypt

    Args: password (plaintext)

    Returns: hashed password
    '''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''
    Verifies a password against its hash

    Args: plaintext pass to verify, stored hashed password

    Returns: Boolean indicating if password is correct
    '''
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    '''
    Creates new user in db

    Args: database session, user creation schema

    Returns: created user model

    Raises: IntegrityError if username or email already exists
    '''
    try:
        hashed_password = hash_password(user.password)

        # Create model
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            skills=user.skills
        )

        # Add and commit new user
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or Email already exists")
    
def get_user_by_username(db: Session, username: str) -> typing.Optional[models.User]:
    '''
    Retrieve user by username

    Args: db session, username to search for

    Returns: user model if found, else returns nothing
    '''
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> typing.Optional[models.User]:
    '''
    Retrieve user by email

    Args: db session, email to search for

    Returns: user model if found, else returns nothing
    '''
    return db.query(models.User).filter(models.User.email == email).first()

def create_service_request(
    db: Session, 
    service_request: schemas.ServiceRequestCreate
) -> models.ServiceRequest:
    '''
    Create new service request

    Args: db session, service creation schema

    Returns: created service request model
    '''
    db_service_request = models.ServiceRequest(
        title=service_request.title,
        description=service_request.description,
        requester_id=service_request.requester_id
    )
    
    db.add(db_service_request)
    db.commit()
    db.refresh(db_service_request)
    
    return db_service_request


def get_service_requests(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> typing.List[models.ServiceRequest]:
    '''
    Retrieve service requests with pagination

    Args: db session, number of records to skip, max num of records to return

    Returns: list of service request models
    '''
    return db.query(models.ServiceRequest).offset(skip).limit(limit).all()
