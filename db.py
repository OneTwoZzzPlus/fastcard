import sqlite3
from pydantic import BaseModel


class Balloon(BaseModel):
    id: int
    places: int
    latitude: float
    longitude: float
    title: str
    is_fast: bool
    power: int


class BalloonAns(BaseModel):
    balloon: Balloon
    distance: int | None
    time: str | None
    is_occupied: bool | None
    is_long: bool | None


conn = sqlite3.connect('balloons_data.db')
cursor = conn.cursor()
balloons: list[Balloon] = []


cursor.execute(
    '''SELECT id, places, point_y, point_x, address, is_fast, power
    FROM balloon WHERE is_current = 1'''
)
for d in cursor.fetchall():
    balloons.append(
        Balloon(
            id=d[0], places=d[1], latitude=d[2], longitude=d[3],
            title=d[4], is_fast=d[5], power=d[6]
        )
    )

