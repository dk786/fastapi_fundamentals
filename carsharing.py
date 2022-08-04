import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, SQLModel, Session, select

from schemas import CarInput, CarOutput, TripInput, Car, Trip

app = FastAPI(title="Car Sharing App")

engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/api/cars")
def cars(size: str | None = None, doors: int | None = None, fuel: str | None = None,
         session: Session = Depends(get_session)) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors == doors)
    if fuel:
        query = query.where(Car.fuel == fuel)

    return session.exec(query).all()


@app.get("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")


def results(result: list, id: int | None = None) -> list:
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No car found matching provided parameters ({id})")


# create a car entry using the Car object.
@app.post("/api/cars/", response_model=CarOutput)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")


@app.put("/api/cars/{id}", response_model=Car)
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


@app.post("/api/cars/{car_id}/trips", response_model=Trip)
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


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
