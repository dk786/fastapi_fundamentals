import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

db = [
    {"id": 1, "size": "s", "doors": 3, "fuel": "petrol"},
    {"id": 2, "size": "s", "doors": 4, "fuel": "electric"},
    {"id": 3, "size": "s", "doors": 4, "fuel": "diesel"},
    {"id": 4, "size": "m", "doors": 3, "fuel": "petrol"},
    {"id": 5, "size": "m", "doors": 4, "fuel": "electric"},
    {"id": 6, "size": "m", "doors": 4, "fuel": "diesel"},
    {"id": 7, "size": "l", "doors": 3, "fuel": "petrol"},
    {"id": 8, "size": "l", "doors": 4, "fuel": "electric"},
    {"id": 9, "size": "l", "doors": 5, "fuel": "diesel"}
]


@app.get("/")
def welcome():
    return {"message": "Welcome to the fast api tutorial"}


@app.get("/api/cars")
def cars(size: str | None = None, doors: int | None = None, fuel: str | None = None) -> list:
    result = db
    if size:
        result = [car for car in result if car['size'] == size]
    if doors:
        result = [car for car in result if car['doors'] == doors]
    if fuel:
        result = [car for car in result if car['fuel'] == fuel]

    return results(result)


@app.get("/api/cars/{id}")
def car_by_id(id: int = None) -> list:
    result = [car for car in db if car['id'] == id]
    return results(result)


def results(result: list) -> list:
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="No car matching provided parameters")


if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)
