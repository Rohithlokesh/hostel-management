from fastapi import FastAPI
from app.routers import students
from app.routers import rooms
from app.routers import allocation
from app.routers import attendance
from app.routers import fees
from app.routers import food
from app.routers import leaves
from app.routers import complaints
from app.routers import admin
from app.routers import audit
from app.routers import dashboard
from app.routers import student_auth
app = FastAPI(
    title="Hostel Management System",
    version= "1.0.0"
)

app.include_router(students.router)
app.include_router(rooms.router)
app.include_router(allocation.router)
app.include_router(attendance.router)
app.include_router(food.router)
app.include_router(leaves.router)
app.include_router(fees.router)
app.include_router(complaints.router)
app.include_router(admin.router)
app.include_router(audit.router)
app.include_router(dashboard.router)
app.include_router(student_auth.router)
@app.get("/")
def home():
    return {"message": "Hostel Management System API"}