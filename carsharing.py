import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, Car

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
    return results(result)


def results(result: list) -> list:
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="No car matching provided parameters")


@app.post("/api/cars/")
def add_car(car: Car):
    db.append(car)
    save_db(db)


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
