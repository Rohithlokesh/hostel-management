
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer


SECRET_KEY = "hostel-management-secret-key-change-this-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(plain_password, hashed_password)


# Create JWT
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Verify JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except JWTError:
        return None


# Admin authentication — keep existing OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login"
)


def get_current_admin(
    token: str = Depends(oauth2_scheme)
):
    username = verify_token(token)

    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return username


# Student authentication — Bearer token scheme
student_bearer = HTTPBearer()


def get_current_student(
    credentials=Depends(student_bearer)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        student_id = payload.get("sub")
        role = payload.get("role")

        if student_id is None or role != "student":
            raise HTTPException(
                status_code=401,
                detail="Invalid student token"
            )

        return int(student_id)

    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired student token"
        )
