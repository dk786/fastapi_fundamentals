import json

from pydantic import BaseModel


class Car(BaseModel):
    id: int
    size: str | None = "m"
    fuel: str | None = "electric"
    doors: int = 4
    transmission: str | None = "automatic"


def load_db() -> list[Car]:
    """Load a list of car objects from a json file"""
    with open("cars.json") as f:
        return [Car.parse_obj(obj) for obj in json.load(f)]


def save_db(cars: list[Car]):
    with open("cars.json", "w") as f:
        # noinspection PyArgumentList
        json.dump([car.dict() for car in cars], f, indent=4)
