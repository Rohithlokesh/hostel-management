from sqlalchemy.orm import Session
from sqlalchemy import func
from app.security import hash_password
from app import models, schemas



def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(
        usn=student.usn,
        name=student.name,
        phone=student.phone,
        email=student.email,
        course=student.course,
        year=student.year,
        gender=student.gender,
        address=student.address,
        guardian_name=student.guardian_name,
        guardian_phone=student.guardian_phone,
        password=hash_password(student.password)
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

def get_students(db: Session):
    return db.query(models.Student).all()
def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter( models.Student.student_id == student_id ).first()
def update_student( db: Session,student_id: int,student: schemas.StudentUpdate):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()

    if db_student is None:
        return None

    for key, value in student.model_dump().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student 
def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.student_id == student_id).first()

    if db_student is None:
        return None

    db.delete(db_student)
    db.commit()

    return db_student
def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(**room.model_dump())

    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    return db_room


def get_rooms(db: Session):
    return db.query(models.Room).all()
def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(
        models.Room.room_id == room_id
    ).first()
def update_room(
    db: Session,
    room_id: int,
    room: schemas.RoomUpdate
):
    db_room = db.query(models.Room).filter(
        models.Room.room_id == room_id
    ).first()

    if db_room is None:
        return None

    for key, value in room.model_dump().items():
        setattr(db_room, key, value)

    db.commit()
    db.refresh(db_room)

    return db_room
def delete_room(db: Session, room_id: int):
    db_room = db.query(models.Room).filter(models.Room.room_id == room_id).first()

    if db_room is None:
        return None

    db.delete(db_room)
    db.commit()

    return db_room
from datetime import date


def create_allocation(
    db: Session,
    allocation: schemas.RoomAllocationCreate
):
    room = db.query(models.Room).filter(
        models.Room.room_id == allocation.room_id
    ).first()

    if room is None:
        return None

    if room.occupied >= room.capacity:
        return None

    db_allocation = models.RoomAllocation(
        student_id=allocation.student_id,
        room_id=allocation.room_id,
        allocated_date=date.fromisoformat(
            allocation.allocated_date
        )
    )

    room.occupied += 1

    if room.occupied >= room.capacity:
        room.status = "Full"
    else:
        room.status = "Available"

    db.add(db_allocation)
    db.commit()
    db.refresh(db_allocation)

    return db_allocation


def get_allocations(db: Session):
    return db.query(models.RoomAllocation).all()
def get_allocation(db: Session, allocation_id: int):
    return db.query(models.RoomAllocation).filter(
        models.RoomAllocation.allocation_id == allocation_id
    ).first()
def delete_allocation(db: Session, allocation_id: int):
    db_allocation = db.query(models.RoomAllocation).filter(
        models.RoomAllocation.allocation_id == allocation_id
    ).first()

    if db_allocation is None:
        return None

    room = db.query(models.Room).filter(
        models.Room.room_id == db_allocation.room_id
    ).first()

    if room and room.occupied > 0:
        room.occupied -= 1
        room.status = "Available"

    db.delete(db_allocation)
    db.commit()

    return db_allocation
def search_student_by_usn(db: Session, usn: str):
    return db.query(models.Student).filter(
        models.Student.usn == usn
    ).first()


def search_students_by_name(db: Session, name: str):
    return db.query(models.Student).filter(
        models.Student.name.ilike(f"%{name}%")
    ).all()

# SEARCH ROOM BY ROOM NUMBER
def search_room_by_number(db: Session, room_number: str):
    return db.query(models.Room).filter(
        models.Room.room_number == room_number
    ).first()


# GET AVAILABLE ROOMS
def get_available_rooms(db: Session):
    return db.query(models.Room).filter(
        models.Room.status == "Available"
    ).all()


# GET ROOMS BY FLOOR
def get_rooms_by_floor(db: Session, floor: int):
    return db.query(models.Room).filter(
        models.Room.floor == floor
    ).all()

# GET ALLOCATION BY STUDENT
def get_allocation_by_student(db: Session, student_id: int):
    return db.query(models.RoomAllocation).filter(
        models.RoomAllocation.student_id == student_id
    ).all()


# GET ALLOCATION BY ROOM
def get_allocation_by_room(db: Session, room_id: int):
    return db.query(models.RoomAllocation).filter(
        models.RoomAllocation.room_id == room_id
    ).all()
def get_available_rooms(db: Session):
    return db.query(models.Room).filter(
        models.Room.occupied < models.Room.capacity
    ).all()
# GET FEES BY STUDENT
def get_fees_by_student(db: Session, student_id: int):
    return db.query(models.Fee).filter(
        models.Fee.student_id == student_id
    ).all()


# GET PENDING FEES
def get_pending_fees(db: Session):
    return db.query(models.Fee).filter(
        models.Fee.status == "Pending"
    ).all()


# GET PAID FEES
def get_paid_fees(db: Session):
    return db.query(models.Fee).filter(
        models.Fee.status == "Paid"
    ).all()


# GET TOTAL PENDING AMOUNT
def get_total_pending_amount(db: Session):
    result = db.query(
        func.sum(models.Fee.amount)
    ).filter(
        models.Fee.status == "Pending"
    ).scalar()

    return result or 0
# GET COMPLAINTS BY STUDENT
def get_complaints_by_student(db: Session, student_id: int):
    return db.query(models.Complaint).filter(
        models.Complaint.student_id == student_id
    ).all()


# GET OPEN COMPLAINTS
def get_open_complaints(db: Session):
    return db.query(models.Complaint).filter(
        models.Complaint.status == "Open"
    ).all()


# GET IN-PROGRESS COMPLAINTS
def get_in_progress_complaints(db: Session):
    return db.query(models.Complaint).filter(
        models.Complaint.status == "In Progress"
    ).all()


# GET RESOLVED COMPLAINTS
def get_resolved_complaints(db: Session):
    return db.query(models.Complaint).filter(
        models.Complaint.status == "Resolved"
    ).all()

# GET ATTENDANCE BY STUDENT
def get_attendance_by_student(db: Session, student_id: int):
    return db.query(models.Attendance).filter(
        models.Attendance.student_id == student_id
    ).all()


# GET ATTENDANCE BY DATE
def get_attendance_by_date(db: Session, date):
    return db.query(models.Attendance).filter(
        models.Attendance.date == date
    ).all()


# GET PRESENT STUDENTS
def get_present_students(db: Session, date):
    return db.query(models.Attendance).filter(
        models.Attendance.date == date,
        models.Attendance.status == "Present"
    ).all()


# GET ABSENT STUDENTS
def get_absent_students(db: Session, date):
    return db.query(models.Attendance).filter(
        models.Attendance.date == date,
        models.Attendance.status == "Absent"
    ).all()
    
# GET FOOD MENU BY DATE
def get_food_by_date(db: Session, food_date):
    return db.query(models.DailyFood).filter(
        models.DailyFood.date == food_date
    ).all()


# GET FOOD BY MEAL TYPE
def get_food_by_meal(db: Session, meal_type: str):
    return db.query(models.DailyFood).filter(
        models.DailyFood.meal_type == meal_type
    ).all()


# GET AVAILABLE FOOD
def get_available_food(db: Session):
    return db.query(models.DailyFood).filter(
        models.DailyFood.availability == "Available"
    ).all()

# GET FOOD CONSUMPTION BY STUDENT
def get_consumption_by_student(db: Session, student_id: int):
    return db.query(models.FoodConsumption).filter(
        models.FoodConsumption.student_id == student_id
    ).all()


# GET CONSUMPTION BY FOOD
def get_consumption_by_food(db: Session, food_id: int):
    return db.query(models.FoodConsumption).filter(
        models.FoodConsumption.food_id == food_id
    ).all()


# GET CONSUMPTION BY STATUS
def get_consumption_by_status(db: Session, status: str):
    return db.query(models.FoodConsumption).filter(
        models.FoodConsumption.status == status
    ).all()

# GET LEAVES BY STUDENT
def get_leaves_by_student(db: Session, student_id: int):
    return db.query(models.Leave).filter(
        models.Leave.student_id == student_id
    ).all()


# GET PENDING LEAVES
def get_pending_leaves(db: Session):
    return db.query(models.Leave).filter(
        models.Leave.status == "Pending"
    ).all()


# GET APPROVED LEAVES
def get_approved_leaves(db: Session):
    return db.query(models.Leave).filter(
        models.Leave.status == "Approved"
    ).all()


# GET REJECTED LEAVES
def get_rejected_leaves(db: Session):
    return db.query(models.Leave).filter(
        models.Leave.status == "Rejected"
    ).all()


# GET AUDIT LOGS BY ADMIN
def get_audit_logs_by_admin(db: Session, admin_id: int):
    return db.query(models.AuditLog).filter(
        models.AuditLog.admin_id == admin_id
    ).all()


# GET AUDIT LOGS BY ACTION
def get_audit_logs_by_action(db: Session, action: str):
    return db.query(models.AuditLog).filter(
        models.AuditLog.action == action
    ).all()


# GET AUDIT LOGS BY TABLE
def get_audit_logs_by_table(db: Session, table_name: str):
    return db.query(models.AuditLog).filter(
        models.AuditLog.table_name == table_name
    ).all()    

# ==============================
# DASHBOARD / REPORTS
# ==============================

def get_dashboard_stats(db: Session):

    total_students = db.query(
        func.count(models.Student.student_id)
    ).scalar()

    total_rooms = db.query(
        func.count(models.Room.room_id)
    ).scalar()

    available_rooms = db.query(
        func.count(models.Room.room_id)
    ).filter(
        models.Room.occupied < models.Room.capacity
    ).scalar()

    occupied_rooms = db.query(
        func.count(models.Room.room_id)
    ).filter(
        models.Room.occupied > 0
    ).scalar()

    total_pending_fees = db.query(
        func.sum(models.Fee.amount)
    ).filter(
        models.Fee.status == "Pending"
    ).scalar()

    pending_leaves = db.query(
        func.count(models.Leave.leave_id)
    ).filter(
        models.Leave.status == "Pending"
    ).scalar()

    open_complaints = db.query(
        func.count(models.Complaint.complaint_id)
    ).filter(
        models.Complaint.status == "Open"
    ).scalar()

    return {
        "total_students": total_students or 0,
        "total_rooms": total_rooms or 0,
        "available_rooms": available_rooms or 0,
        "occupied_rooms": occupied_rooms or 0,
        "total_pending_fees": float(total_pending_fees or 0),
        "pending_leaves": pending_leaves or 0,
        "open_complaints": open_complaints or 0
    }