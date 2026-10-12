from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from datetime import date

from app.database import get_db
from app.models import Attendance
from app.schemas import AttendanceCreate, AttendanceResponse


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/", response_model=AttendanceResponse)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    new_attendance = Attendance(
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status,
        marked_by=attendance.marked_by
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance


@router.get("/", response_model=list[AttendanceResponse])
def get_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).all()


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_by_id(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.attendance_id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    return attendance


@router.delete("/{attendance_id}")
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    attendance = db.query(Attendance).filter(
        Attendance.attendance_id == attendance_id
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=404,
            detail="Attendance record not found"
        )

    db.delete(attendance)
    db.commit()

    return {"message": "Attendance deleted successfully"}
@router.get("/{attendance_id}")
# ATTENDANCE BY STUDENT
@router.get("/student/{student_id}")
def get_attendance_by_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_attendance_by_student(db, student_id)


# ATTENDANCE BY DATE
@router.get("/date/{date}")
def get_attendance_by_date(
    date: date,
    db: Session = Depends(get_db)
):
    return crud.get_attendance_by_date(db, date)


# PRESENT STUDENTS
@router.get("/present/{date}")
def get_present_students(
    date: date,
    db: Session = Depends(get_db)
):
    return crud.get_present_students(db, date)


# ABSENT STUDENTS
@router.get("/absent/{date}")
def get_absent_students(
    date: date,
    db: Session = Depends(get_db)
):
    return crud.get_absent_students(db, date)
