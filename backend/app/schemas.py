from pydantic import BaseModel
from datetime import date
class StudentCreate(BaseModel):
    name: str
    usn: str
    phone: str
    email: str
    course: str
    year: int
    gender: str
    address: str
    guardian_name: str
    guardian_phone: str
    password: str
class Student(StudentCreate):
        student_id: int
        class Config:
            from_attributes = True
class StudentUpdate(BaseModel):
    name: str
    phone: str
    email: str
    course: str
    year: int
    gender: str
    address: str
    guardian_name: str
    guardian_phone: str
    password:str
class RoomCreate(BaseModel):
    room_number: str
    floor: int
    capacity: int
    occupied: int = 0
    room_type: str
    status: str = "Available"
    


class Room(RoomCreate):
    room_id: int

    class Config:
        from_attributes = True
class RoomUpdate(BaseModel):
    room_number: str
    floor: int
    capacity: int
    occupied: int
    room_type: str
    status: str
class RoomAllocationCreate(BaseModel):
    student_id: int
    room_id: int
    allocated_date: str


class RoomAllocation(RoomAllocationCreate):
    allocation_id: int

    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    student_id: int
    date: date
    status: str
    marked_by: int | None = None


class AttendanceResponse(BaseModel):
    attendance_id: int
    student_id: int
    date: date
    status: str
    marked_by: int | None = None

    class Config:
        from_attributes = True
from datetime import date, datetime
from pydantic import BaseModel


# -------------------------
# DAILY FOOD
# -------------------------

class DailyFoodCreate(BaseModel):
    date: date
    meal_type: str
    menu: str | None = None
    availability: str = "Available"
    created_by: int | None = None


class DailyFoodResponse(BaseModel):
    food_id: int
    date: date
    meal_type: str
    menu: str | None = None
    availability: str
    created_by: int | None = None

    class Config:
        from_attributes = True


# -------------------------
# FOOD CONSUMPTION
# -------------------------

class FoodConsumptionCreate(BaseModel):
    student_id: int
    food_id: int
    status: str = "Taken"


class FoodConsumptionResponse(BaseModel):
    consumption_id: int
    student_id: int
    food_id: int
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
class LeaveCreate(BaseModel):
    student_id: int
    start_date: date
    end_date: date
    reason: str | None = None
    status: str = "Pending"
    applied_date: date


class LeaveResponse(BaseModel):
    leave_id: int
    student_id: int
    start_date: date
    end_date: date
    reason: str | None = None
    status: str
    applied_date: date

    class Config:
        from_attributes = True

class LeaveUpdate(BaseModel):
    status: str


class ComplaintCreate(BaseModel):
    student_id: int
    complaint: str
    status: str = "Pending"


class ComplaintResponse(BaseModel):
    complaint_id: int
    student_id: int
    complaint: str
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class FeeCreate(BaseModel):
    student_id: int
    amount: float
    payment_date: date | None = None
    due_date: date | None = None
    status: str = "Pending"


class FeeResponse(BaseModel):
    fee_id: int
    student_id: int
    amount: float
    payment_date: date | None = None
    due_date: date | None = None
    status: str

    class Config:
        from_attributes = True
        
class AdminCreate(BaseModel):
    username: str
    password: str


class AdminResponse(BaseModel):
    admin_id: int
    username: str

    class Config:
        from_attributes = True
        
class AdminLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    
class AuditLogCreate(BaseModel):
    admin_id: int
    action: str
    table_name: str | None = None
    details: str | None = None


class AuditLogResponse(BaseModel):
    log_id: int
    admin_id: int
    action: str
    timestamp: datetime | None = None
    table_name: str | None = None
    details: str | None = None

    class Config:
        from_attributes = True
class StudentLogin(BaseModel):
    usn: str
    password: str