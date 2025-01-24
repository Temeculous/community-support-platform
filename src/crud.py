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
    
