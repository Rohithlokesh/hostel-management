from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud


router = APIRouter(
    prefix="/allocations",
    tags=["Room Allocation"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_room_allocation(
    allocation: schemas.RoomAllocationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_allocation(db, allocation)


@router.get("/")
def get_all_allocations(
    db: Session = Depends(get_db)
):
    return crud.get_allocations(db)
@router.get("/{allocation_id}")
def get_allocation_by_id(
    allocation_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_allocation(db, allocation_id)
@router.delete("/{allocation_id}")
def delete_allocation(
    allocation_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_allocation(db, allocation_id)
@router.get("/{allocation_id}")
# SEARCH ALLOCATION BY STUDENT
@router.get("/student/{student_id}")
def get_allocation_by_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_allocation_by_student(db, student_id)


# SEARCH ALLOCATION BY ROOM
@router.get("/room/{room_id}")
def get_allocation_by_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_allocation_by_room(db, room_id)
@router.get("/available-rooms")
def get_available_rooms(
    db: Session = Depends(get_db)
):
    return crud.get_available_rooms(db)@router.get("/available-rooms")
