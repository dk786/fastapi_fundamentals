import json

from pydantic import BaseModel


class CarInput(BaseModel):
    size: str | None = "m"
    fuel: str | None = "electric"
    doors: int = 4
    transmission: str | None = "automatic"


class CarOutput(CarInput):
    id: int


def load_db() -> list[CarOutput]:
    """Load a list of car objects from a json file"""
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]


def save_db(cars: list[CarOutput]):
    with open("cars.json", "w") as f:
        # noinspection PyArgumentList
        json.dump([car.dict() for car in cars], f, indent=4)
