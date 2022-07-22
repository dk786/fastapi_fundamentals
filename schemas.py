from pydantic import BaseModel


class Car(BaseModel):
    id: int
    size: str | None = "m"
    fuel: str | None = "electric"
    doors: int = 4
    transmission: str | None = "automatic"

