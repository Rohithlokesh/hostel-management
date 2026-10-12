from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app import crud

from app.database import get_db
from app.models import DailyFood, FoodConsumption
from app.schemas import (
    DailyFoodCreate,
    DailyFoodResponse,
    FoodConsumptionCreate,
    FoodConsumptionResponse
)


router = APIRouter(
    prefix="/food",
    tags=["Food Management"]
)


# =========================================================
# DAILY FOOD
# =========================================================

@router.post(
    "/menu",
    response_model=DailyFoodResponse
)
def create_food_menu(
    food: DailyFoodCreate,
    db: Session = Depends(get_db)
):

    new_food = DailyFood(
        date=food.date,
        meal_type=food.meal_type,
        menu=food.menu,
        availability=food.availability,
        created_by=food.created_by
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return new_food


@router.get(
    "/menu",
    response_model=list[DailyFoodResponse]
)
def get_food_menus(
    db: Session = Depends(get_db)
):

    return db.query(DailyFood).all()


@router.get(
    "/menu/{food_id}",
    response_model=DailyFoodResponse
)
def get_food_menu(
    food_id: int,
    db: Session = Depends(get_db)
):

    food = db.query(DailyFood).filter(
        DailyFood.food_id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food menu not found"
        )

    return food


@router.delete("/menu/{food_id}")
def delete_food_menu(
    food_id: int,
    db: Session = Depends(get_db)
):

    food = db.query(DailyFood).filter(
        DailyFood.food_id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food menu not found"
        )

    db.delete(food)
    db.commit()

    return {
        "message": "Food menu deleted successfully"
    }


# =========================================================
# FOOD CONSUMPTION
# =========================================================

@router.post(
    "/consumption",
    response_model=FoodConsumptionResponse
)
def create_food_consumption(
    consumption: FoodConsumptionCreate,
    db: Session = Depends(get_db)
):

    # Check student
    from app.models import Student

    student = db.query(Student).filter(
        Student.student_id == consumption.student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check food menu
    food = db.query(DailyFood).filter(
        DailyFood.food_id == consumption.food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Food menu not found"
        )

    new_consumption = FoodConsumption(
        student_id=consumption.student_id,
        food_id=consumption.food_id,
        status=consumption.status
    )

    db.add(new_consumption)
    db.commit()
    db.refresh(new_consumption)

    return new_consumption


@router.get(
    "/consumption",
    response_model=list[FoodConsumptionResponse]
)
def get_food_consumption(
    db: Session = Depends(get_db)
):

    return db.query(FoodConsumption).all()


@router.get(
    "/consumption/{consumption_id}",
    response_model=FoodConsumptionResponse
)
def get_food_consumption_by_id(
    consumption_id: int,
    db: Session = Depends(get_db)
):

    consumption = db.query(FoodConsumption).filter(
        FoodConsumption.consumption_id == consumption_id
    ).first()

    if not consumption:
        raise HTTPException(
            status_code=404,
            detail="Food consumption record not found"
        )

    return consumption


@router.delete("/consumption/{consumption_id}")
def delete_food_consumption(
    consumption_id: int,
    db: Session = Depends(get_db)
):

    consumption = db.query(FoodConsumption).filter(
        FoodConsumption.consumption_id == consumption_id
    ).first()

    if not consumption:
        raise HTTPException(
            status_code=404,
            detail="Food consumption record not found"
        )

    db.delete(consumption)
    db.commit()

    return {
        "message": "Food consumption deleted successfully"
    }

@router.get("/menu/{food_id}")
# MENU BY DATE
@router.get("/menu/date/{food_date}")
def get_food_by_date(
    food_date: date,
    db: Session = Depends(get_db)
):
    return crud.get_food_by_date(db, food_date)


# MENU BY MEAL TYPE
@router.get("/menu/meal/{meal_type}")
def get_food_by_meal(
    meal_type: str,
    db: Session = Depends(get_db)
):
    return crud.get_food_by_meal(db, meal_type)


# AVAILABLE FOOD
@router.get("/menu/available")
def get_available_food(
    db: Session = Depends(get_db)
):
    return crud.get_available_food(db)

@router.get("/consumption/{consumption_id}")
# CONSUMPTION BY STUDENT
@router.get("/consumption/student/{student_id}")
def get_consumption_by_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_consumption_by_student(db, student_id)


# CONSUMPTION BY FOOD
@router.get("/consumption/food/{food_id}")
def get_consumption_by_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_consumption_by_food(db, food_id)


# CONSUMPTION BY STATUS
@router.get("/consumption/status/{status}")
def get_consumption_by_status(
    status: str,
    db: Session = Depends(get_db)
):
    return crud.get_consumption_by_status(db, status)