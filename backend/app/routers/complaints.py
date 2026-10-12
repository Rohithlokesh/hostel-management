from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Complaint, Student
from app.schemas import ComplaintCreate, ComplaintResponse
from app import crud


router = APIRouter(
    prefix="/complaints",
    tags=["Complaint Management"]
)


# CREATE COMPLAINT
@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db)
):
    # Check whether student exists
    student = db.query(Student).filter(
        Student.student_id == complaint.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_complaint = Complaint(
        student_id=complaint.student_id,
        complaint=complaint.complaint,
        status=complaint.status
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


# GET ALL COMPLAINTS
@router.get("/", response_model=list[ComplaintResponse])
def get_complaints(
    db: Session = Depends(get_db)
):
    return db.query(Complaint).all()


# GET COMPLAINT BY ID
@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    return complaint


# UPDATE COMPLAINT STATUS
@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(
    complaint_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    if status not in ["Open", "In Progress", "Resolved"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Open, In Progress or Resolved"
        )

    complaint.status = status

    db.commit()
    db.refresh(complaint)

    return complaint


# DELETE COMPLAINT
@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.complaint_id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    db.delete(complaint)
    db.commit()

    return {
        "message": "Complaint deleted successfully"
    }
@router.get("/{complaint_id}")
# COMPLAINTS BY STUDENT
@router.get("/student/{student_id}")
def get_complaints_by_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_complaints_by_student(db, student_id)


# OPEN COMPLAINTS
@router.get("/status/open")
def get_open_complaints(
    db: Session = Depends(get_db)
):
    return crud.get_open_complaints(db)


# IN-PROGRESS COMPLAINTS
@router.get("/status/in-progress")
def get_in_progress_complaints(
    db: Session = Depends(get_db)
):
    return crud.get_in_progress_complaints(db)


# RESOLVED COMPLAINTS
@router.get("/status/resolved")
def get_resolved_complaints(
    db: Session = Depends(get_db)
):
    return crud.get_resolved_complaints(db)