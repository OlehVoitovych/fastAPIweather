import time
from fastapi import FastAPI, HTTPException, Query
import aiohttp
from Creds import API_KEY
import AWSs3

app = FastAPI()

async def fetch_weather_data(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
                else:
                    raise HTTPException(
                        status_code=response.status, detail="Failed to fetch weather data."
                    )
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=500, detail=f"Network error: {e}")


@app.get("/weather")
async def get_weather(city: str = Query(..., description="The name of the city to fetch weather for")):

    city = city[0].upper() + city[1:].lower()
    try:

        ts = int(round(time.time()))

        if await AWSs3.five_minute_check(ts, city):
            return await AWSs3.get_weather_from_s3()
        else:
            weather_data = await fetch_weather_data(city)
            await AWSs3.save_to_s3(weather_data, ts)
            return weather_data

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
