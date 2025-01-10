import time
from fastapi import FastAPI, HTTPException, Query
import WeatherAPI.openWeatherAPI
import AWS_services.DDB_filter
import AWS_services.DDB_log
import AWS_services.S3_load_item
import AWS_services.S3_get_item

app = FastAPI()

async def logic(city):
    ts = int(round(time.time()))
    if await AWS_services.DDB_filter.five_minute_check(ts, city):
        return await AWS_services.S3_get_item.get_weather_from_s3()
    else:
        weather_data = await WeatherAPI.openWeatherAPI.fetch_weather_data(city.title())
        await AWS_services.S3_load_item.save_to_s3(weather_data, ts)
        return weather_data

@app.get("/weather")
async def get_weather(city: str = Query(..., description="The name of the city to fetch weather for")):
    try:
        city = city[0].upper() + city[1:].lower()
        return await logic(city)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
