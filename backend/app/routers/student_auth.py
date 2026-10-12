from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security import get_current_student

from sqlalchemy import func


from datetime import date
from pydantic import BaseModel


from app.database import get_db
from app import models, schemas
from app.security import verify_password, create_access_token

router = APIRouter(
    prefix="/student",
    tags=["Student Authentication"]
)


@router.post("/login")
def student_login(
    data: schemas.StudentLogin,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.usn == data.usn
    ).first()

    if not student:
        raise HTTPException(
            status_code=401,
            detail="Invalid USN or password"
        )

    if not student.password or not verify_password(
        data.password, student.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid USN or password"
        )

    token = create_access_token({
        "sub": str(student.student_id),
        "role": "student"
    })

    return {
        "message": "Student login successful",
        "access_token": token,
        "token_type": "bearer"
    }
    

@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "student_id": student.student_id,
        "usn": student.usn,
        "name": student.name,
        "phone": student.phone,
        "email": student.email,
        "course": student.course,
        "year": student.year,
        "gender": student.gender,
        "address": student.address,
        "guardian_name": student.guardian_name,
        "guardian_phone": student.guardian_phone
    }

# SUBMIT A COMPLAINT
@router.post("/my-complaints")
def create_my_complaint(
    complaint: str,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    new_complaint = models.Complaint(
        student_id=student_id,
        complaint=complaint,
        status="Open"
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


# VIEW MY COMPLAINTS
@router.get("/my-complaints")
def get_my_complaints(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    return db.query(models.Complaint).filter(
        models.Complaint.student_id == student_id
    ).all()

@router.get("/my-room")
def get_my_room(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    allocation = db.query(models.RoomAllocation).filter(
        models.RoomAllocation.student_id == student_id
    ).first()

    if allocation is None:
        raise HTTPException(
            status_code=404,
            detail="No room allocated to this student"
        )

    room = db.query(models.Room).filter(
        models.Room.room_id == allocation.room_id
    ).first()

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room details not found"
        )

    return {
        "allocation_id": allocation.allocation_id,
        "allocated_date": allocation.allocated_date,
        "room_id": room.room_id,
        "room_number": room.room_number,
        "floor": room.floor,
        "capacity": room.capacity,
        "occupied": room.occupied,
        "room_type": room.room_type,
        "status": room.status
    }

@router.get("/my-fees")
def get_my_fees(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    fees = db.query(models.Fee).filter(
        models.Fee.student_id == student_id
    ).all()

    return fees

@router.get("/my-attendance")
def get_my_attendance(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    attendance_records = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).order_by(models.Attendance.date.desc()).all()

    return attendance_records

@router.get("/my-food-menu")
def get_my_food_menu(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    food_menu = db.query(models.DailyFood).order_by(
        models.DailyFood.date.desc()
    ).all()

    return food_menu

class StudentLeaveRequest(BaseModel):
    start_date: date
    end_date: date
    reason: str


@router.post("/my-leaves")
def apply_my_leave(
    data: StudentLeaveRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )

    new_leave = models.Leave(
        student_id=student_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="Pending",
        applied_date=date.today()
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave

@router.get("/my-leaves")
def get_my_leaves(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    leave_records = db.query(models.Leave).filter(
        models.Leave.student_id == student_id
    ).order_by(models.Leave.applied_date.desc()).all()

    return leave_records

from pydantic import BaseModel

class FoodConsumptionRequest(BaseModel):
    food_id: int
    status: str


@router.post("/my-food-consumption")
def mark_food_consumption(
    data: FoodConsumptionRequest,
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    if data.status not in ["Taken", "Not Taken"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be Taken or Not Taken"
        )

    food = db.query(models.DailyFood).filter(
        models.DailyFood.food_id == data.food_id
    ).first()

    if food is None:
        raise HTTPException(
            status_code=404,
            detail="Food menu not found"
        )

    record = models.FoodConsumption(
        student_id=student_id,
        food_id=data.food_id,
        status=data.status
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get("/my-food-consumption")
def get_my_food_consumption(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    records = db.query(models.FoodConsumption).filter(
        models.FoodConsumption.student_id == student_id
    ).order_by(
        models.FoodConsumption.created_at.desc()
    ).all()

    return records

@router.get("/dashboard")
def get_student_dashboard(
    db: Session = Depends(get_db),
    student_id: int = Depends(get_current_student)
):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    total_fees = db.query(models.Fee).filter(
        models.Fee.student_id == student_id
    ).count()

    pending_fees = db.query(models.Fee).filter(
        models.Fee.student_id == student_id,
        models.Fee.status == "Pending"
    ).count()

    total_complaints = db.query(models.Complaint).filter(
        models.Complaint.student_id == student_id
    ).count()

    total_leaves = db.query(models.Leave).filter(
        models.Leave.student_id == student_id
    ).count()

    total_attendance = db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).count()

    return {
        "student_name": student.name,
        "usn": student.usn,
        "total_fee_records": total_fees,
        "pending_fee_records": pending_fees,
        "total_complaints": total_complaints,
        "total_leave_requests": total_leaves,
        "total_attendance_records": total_attendance
    }





