from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from temperature import schemas
from temperature.crud import update_temperature

router = APIRouter()


@router.post(
    "/temperature/update/",
    response_model=schemas.TemperatureUpdate,
    summary="Update temperature",
    description="Update the current temperature for all cities in database",
)
async def update_temperature_for_cities(db: AsyncSession = Depends(get_db)):
    result = await update_temperature(db)
    cities_total = result["updated"] + len(result["missing"])

    return {
        "cities_total": cities_total,
        "updated": result["updated"],
        "missing": result["missing"],
    }
