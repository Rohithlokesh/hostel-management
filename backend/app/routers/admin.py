from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.security import get_current_admin

from app.database import get_db
from app.models import Admin
from app.schemas import (
    AdminCreate,
    AdminResponse,
    AdminLogin,
    TokenResponse
)
from app.security import (
    hash_password,
    verify_password,
    create_access_token
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin Management"]
)


# =========================================================
# CREATE ADMIN
# =========================================================

@router.post(
    "/",
    response_model=AdminResponse
)
def create_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db)
):

    existing_admin = db.query(Admin).filter(
        Admin.username == admin.username
    ).first()

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(
        admin.password
    )

    new_admin = Admin(
        username=admin.username,
        password=hashed_password
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def admin_login(
    login: AdminLogin,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.username == login.username
    ).first()

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        login.password,
        admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": admin.username,
            "admin_id": admin.admin_id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================================================
# GET ALL ADMINS
# =========================================================

@router.get(
    "/",
    response_model=list[AdminResponse]
)
def get_admins(
    db: Session = Depends(get_db)
):

    return db.query(Admin).all()


# =========================================================
# GET ADMIN BY ID
# =========================================================

@router.get(
    "/{admin_id}",
    response_model=AdminResponse
)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.admin_id == admin_id
    ).first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return admin


# =========================================================
# DELETE ADMIN
# =========================================================

@router.delete("/{admin_id}")
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.admin_id == admin_id
    ).first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    db.delete(admin)
    db.commit()

    return {
        "message": "Admin deleted successfully"
    }
@router.get("/protected")
def protected_route(
    current_admin: str = Depends(get_current_admin)
):
    return {
        "message": "Access granted",
        "admin": current_admin
    }