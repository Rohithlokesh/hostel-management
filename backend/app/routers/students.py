from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session




from app.database import SessionLocal
from app import schemas, crud

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/")
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)
@router.get("/")
def get_all_students(db: Session = Depends(get_db)):
    return crud.get_students(db)
@router.get("/{student_id}")
def get_student_by_id(student_id: int,db: Session = Depends(get_db)):
    return crud.get_student(db, student_id)
@router.put("/{student_id}")
def update_student( student_id: int,student: schemas.StudentUpdate,db: Session = Depends(get_db)):
    return crud.update_student(db, student_id, student)
@router.delete("/{student_id}")
def delete_student(student_id: int,db: Session = Depends(get_db)):
    return crud.delete_student(db, student_id)

@router.get("/{student_id}")
# SEARCH STUDENT BY USN
@router.get("/search/usn/{usn}")
def search_student_by_usn(
    usn: str,
    db: Session = Depends(get_db)
):
    return crud.search_student_by_usn(db, usn)


# SEARCH STUDENT BY NAME
@router.get("/search/name/{name}")
def search_students_by_name(
    name: str,
    db: Session = Depends(get_db)
):
    return crud.search_students_by_name(db, name)


