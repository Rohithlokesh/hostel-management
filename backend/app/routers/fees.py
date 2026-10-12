from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Fee, Student
from app.schemas import FeeCreate, FeeResponse
from app import crud


router = APIRouter(
    prefix="/fees",
    tags=["Fee Management"]
)


# CREATE FEE
@router.post("/", response_model=FeeResponse)
def create_fee(
    fee: FeeCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.student_id == fee.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    new_fee = Fee(
        student_id=fee.student_id,
        amount=fee.amount,
        payment_date=fee.payment_date,
        due_date=fee.due_date,
        status=fee.status
    )

    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)

    return new_fee


# GET ALL FEES
@router.get("/", response_model=list[FeeResponse])
def get_fees(
    db: Session = Depends(get_db)
):
    return db.query(Fee).all()


# GET FEE BY ID
@router.get("/{fee_id}", response_model=FeeResponse)
def get_fee(
    fee_id: int,
    db: Session = Depends(get_db)
):

    fee = db.query(Fee).filter(
        Fee.fee_id == fee_id
    ).first()

    if not fee:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    return fee


# DELETE FEE
@router.delete("/{fee_id}")
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db)
):

    fee = db.query(Fee).filter(
        Fee.fee_id == fee_id
    ).first()

    if not fee:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    db.delete(fee)
    db.commit()

    return {
        "message": "Fee deleted successfully"
    }
@router.get("/{fee_id}")
# FEES OF A PARTICULAR STUDENT
@router.get("/student/{student_id}")
def get_fees_by_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_fees_by_student(db, student_id)


# PENDING FEES
@router.get("/pending")
def get_pending_fees(
    db: Session = Depends(get_db)
):
    return crud.get_pending_fees(db)


# PAID FEES
@router.get("/paid")
def get_paid_fees(
    db: Session = Depends(get_db)
):
    return crud.get_paid_fees(db)


# TOTAL PENDING AMOUNT
@router.get("/pending/total")
def get_total_pending_amount(
    db: Session = Depends(get_db)
):
    return {
        "total_pending_amount":
        crud.get_total_pending_amount(db)
    }