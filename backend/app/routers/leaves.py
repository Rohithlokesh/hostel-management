from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud

from app.database import get_db
from app.models import Leave, Student
from app.schemas import LeaveCreate, LeaveResponse, LeaveUpdate


router = APIRouter(
    prefix="/leaves",
    tags=["Leave Management"]
)


# CREATE LEAVE
@router.post("/", response_model=LeaveResponse)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db)
):

    # Check whether student exists
    student = db.query(Student).filter(
        Student.student_id == leave.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check date
    if leave.end_date < leave.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    new_leave = Leave(
        student_id=leave.student_id,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status=leave.status,
        applied_date=leave.applied_date
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave


# GET ALL LEAVES
@router.get("/", response_model=list[LeaveResponse])
def get_leaves(
    db: Session = Depends(get_db)
):

    return db.query(Leave).all()


# GET LEAVE BY ID
@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):

    leave = db.query(Leave).filter(
        Leave.leave_id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    return leave


# UPDATE LEAVE STATUS
@router.put("/{leave_id}", response_model=LeaveResponse)
def update_leave_status(
    leave_id: int,
    leave_update: LeaveUpdate,
    db: Session = Depends(get_db)
):

    leave = db.query(Leave).filter(
        Leave.leave_id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    if leave_update.status not in ["Pending", "Approved", "Rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Pending, Approved or Rejected"
        )

    leave.status = leave_update.status

    db.commit()
    db.refresh(leave)

    return leave


# DELETE LEAVE
@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db)
):

    leave = db.query(Leave).filter(
        Leave.leave_id == leave_id
    ).first()

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    db.delete(leave)
    db.commit()

    return {
        "message": "Leave deleted successfully"
    }
    
@router.get("/{leave_id}")
# LEAVES BY STUDENT
@router.get("/student/{student_id}")
def get_leaves_by_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_leaves_by_student(db, student_id)


# PENDING LEAVES
@router.get("/status/pending")
def get_pending_leaves(
    db: Session = Depends(get_db)
):
    return crud.get_pending_leaves(db)


# APPROVED LEAVES
@router.get("/status/approved")
def get_approved_leaves(
    db: Session = Depends(get_db)
):
    return crud.get_approved_leaves(db)


# REJECTED LEAVES
@router.get("/status/rejected")
def get_rejected_leaves(
    db: Session = Depends(get_db)
):
    return crud.get_rejected_leaves(db)
