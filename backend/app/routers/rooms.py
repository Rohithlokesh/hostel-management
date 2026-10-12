from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_room(
    room: schemas.RoomCreate,
    db: Session = Depends(get_db)
):
    return crud.create_room(db, room)


@router.get("/")
def get_all_rooms(
    db: Session = Depends(get_db)
):
    return crud.get_rooms(db)
@router.get("/{room_id}")
def get_room_by_id(
    room_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_room(db, room_id)
@router.put("/{room_id}")
def update_room(
    room_id: int,
    room: schemas.RoomUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_room(db, room_id, room)
@router.delete("/{room_id}")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_room(db, room_id)

@router.get("/{room_id}")
# SEARCH ROOM BY ROOM NUMBER
@router.get("/search/number/{room_number}")
def search_room_by_number(
    room_number: str,
    db: Session = Depends(get_db)
):
    return crud.search_room_by_number(db, room_number)


# GET AVAILABLE ROOMS
@router.get("/available")
def get_available_rooms(
    db: Session = Depends(get_db)
):
    return crud.get_available_rooms(db)


# GET ROOMS BY FLOOR
@router.get("/floor/{floor}")
def get_rooms_by_floor(
    floor: int,
    db: Session = Depends(get_db)
):
    return crud.get_rooms_by_floor(db, floor)