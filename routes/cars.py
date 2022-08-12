from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from routes.auth import get_current_user
from schemas import CarOutput, Car, CarInput, TripInput, Trip, User

router = APIRouter(prefix="/api/cars")


@router.get("/{id}", response_model=CarOutput)
def change_car(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")


@router.get("/")
def get_cars(size: str | None = None, doors: int | None = None, fuel: str | None = None,
             session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors == doors)
    if fuel:
        query = query.where(Car.fuel == fuel)

    return session.exec(query).all()


@router.post("/", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session),
            user: User = Depends(get_current_user)) -> Car:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@router.delete("/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")


def results(result: list, id: int | None = None) -> list:
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No car found matching provided parameters ({id})")


# create a car entry using the Car object.


@router.post("/{car_id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput,
             session: Session = Depends(get_session)) -> Trip:
    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.from_orm(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=403, detail=f"No car with id = {car_id}")


@router.put("/{id}", response_model=Car)
def change_car(id: int, new_car: CarInput,
               session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        car.size = new_car.size
        car.fuel = new_car.fuel
        car.transmission = new_car.transmission
        car.doors = new_car.doors
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")
