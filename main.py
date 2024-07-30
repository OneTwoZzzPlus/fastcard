import uvicorn
from fastapi import FastAPI
from config import HOST, PORT
import db
import gis

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "404"}


@app.get("/balloons")
async def get_all_balloons():
    return db.balloons


@app.get("/point")
async def get_nearest_balloons(lat: float = 55.694814, lon: float = 37.524875, count: int = 5):
    return await gis.get_nearest_balloons(lat, lon, count)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
