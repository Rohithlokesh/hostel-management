from sqlalchemy import Column, Integer, String, Enum, Text, Date, DECIMAL, TIMESTAMP, ForeignKey,DATETIME,func
from app.database import Base



class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    usn = Column(String(20), unique=True, nullable=False)
    phone = Column(String(15))
    email = Column(String(100), unique=True)
    course = Column(String(50))
    year = Column(Integer)
    gender = Column(Enum("Male", "Female", "Other"))
    address = Column(Text)
    guardian_name = Column(String(100))
    guardian_phone = Column(String(15))
    created_at = Column(TIMESTAMP, nullable=True)
    password = Column(String(255),nullable=True)


class Room(Base):
    __tablename__ = "rooms"

    room_id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10), unique=True, nullable=False)
    floor = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    occupied = Column(Integer, default=0)
    room_type = Column(Enum("Single", "Double", "Triple"), nullable=False)
    status = Column(Enum("Available", "Full"), default="Available")


class RoomAllocation(Base):
    __tablename__ = "room_allocation"

    allocation_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    allocated_date = Column(Date, nullable=True)




class Attendance(Base):
    __tablename__ = "attendance"

    attendance_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    marked_by = Column(Integer, ForeignKey("admin.admin_id"))
class DailyFood(Base):
    __tablename__ = "daily_food"

    food_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    meal_type = Column(String(30), nullable=False)
    menu = Column(String(255))
    availability = Column(String(30), default="Available")
    created_by = Column(Integer, ForeignKey("admin.admin_id"))


class FoodConsumption(Base):
    __tablename__ = "food_consumption"

    consumption_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    food_id = Column(Integer, ForeignKey("daily_food.food_id"), nullable=False)
    status = Column(String(30), default="Taken")
    created_at = Column(DATETIME, server_default=func.now())
class Leave(Base):
    __tablename__ = "leaves"

    leave_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String(255))
    status = Column(String(30), default="Pending")
    applied_date = Column(Date, nullable=False)


class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    complaint = Column(String(255), nullable=False)
    status = Column(String(30), default="Pending")
    created_at = Column(DATETIME, server_default=func.now())
    
    
class Fee(Base):
    __tablename__ = "fees"

    fee_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(
        Integer,
        ForeignKey("students.student_id"),
        nullable=False
    )
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    status = Column(String(20), default="Pending")


class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_log"

    log_id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(
        Integer,
        ForeignKey("admin.admin_id"),
        nullable=False
    )
    action = Column(String(100))
    timestamp = Column(
        DATETIME,
        server_default=func.now()
    )
    table_name = Column(String(100))
    details = Column(Text)
