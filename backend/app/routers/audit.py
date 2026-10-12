from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud

from app.database import get_db
from app.models import AuditLog, Admin
from app.schemas import AuditLogCreate, AuditLogResponse


router = APIRouter(
    prefix="/audit",
    tags=["Audit Log"]
)


# CREATE AUDIT LOG
@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    log: AuditLogCreate,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.admin_id == log.admin_id
    ).first()

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    new_log = AuditLog(
        admin_id=log.admin_id,
        action=log.action,
        table_name=log.table_name,
        details=log.details
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


# GET ALL AUDIT LOGS
@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(
    db: Session = Depends(get_db)
):
    return db.query(AuditLog).all()


# GET AUDIT LOG BY ID
@router.get("/{log_id}", response_model=AuditLogResponse)
def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    log = db.query(AuditLog).filter(
        AuditLog.log_id == log_id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found"
        )

    return log


# DELETE AUDIT LOG
@router.delete("/{log_id}")
def delete_audit_log(
    log_id: int,
    db: Session = Depends(get_db)
):

    log = db.query(AuditLog).filter(
        AuditLog.log_id == log_id
    ).first()

    if not log:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found"
        )

    db.delete(log)
    db.commit()

    return {
        "message": "Audit log deleted successfully"
    }
    
@router.get("/{log_id}")
# AUDIT LOGS BY ADMIN
@router.get("/admin/{admin_id}")
def get_audit_logs_by_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_audit_logs_by_admin(db, admin_id)


# AUDIT LOGS BY ACTION
@router.get("/action/{action}")
def get_audit_logs_by_action(
    action: str,
    db: Session = Depends(get_db)
):
    return crud.get_audit_logs_by_action(db, action)


# AUDIT LOGS BY TABLE
@router.get("/table/{table_name}")
def get_audit_logs_by_table(
    table_name: str,
    db: Session = Depends(get_db)
):
    return crud.get_audit_logs_by_table(db, table_name)