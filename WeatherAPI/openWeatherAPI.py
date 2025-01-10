from fastapi import HTTPException
import aiohttp
from Config import config

async def fetch_weather_data(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.BaseConfig.API_KEY}"
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