import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, CarInput, CarOutput

app = FastAPI()
db = load_db()


@app.get("/api/cars")
def cars(size: str | None = None, doors: int | None = None, fuel: str | None = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors == doors]
    if fuel:
        result = [car for car in result if car.fuel == fuel]

    return results(result)


@app.get("/api/cars/{id}")
def car_by_id(id: int = None) -> list:
    result = [car for car in db if car.id == id]
    return results(result, id)


def results(result: list, id: int | None = None) -> list:
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No car found matching provided parameters ({id})")


# create a car entry using the Car object.
@app.post("/api/cars/", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    match = [car for car in db if car.id == id]
    if match:
        car = match[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")


@app.put("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_car: CarInput) -> CarOutput:
    match = [car for car in db if car.id == id]
    if match:
        car = match[0]
        car.fuel = new_car.fuel
        car.size = new_car.size
        car.doors = new_car.doors
        car.transmission = new_car.transmission
        save_db(db)
        return match[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car with Id {id} found.")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
