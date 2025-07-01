from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from cities import schemas, models


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    new_city = models.City(**city.model_dump())
    db.add(new_city)

    try:
        await db.commit()
        await db.refresh(new_city)
    except IntegrityError:
        await db.rollback()
        raise

    return new_city


async def get_city_by_id(db: AsyncSession, city_id: int):
    stmt = select(models.City).where(models.City.id == city_id)
    result = await db.execute(stmt)
    city = result.scalar_one_or_none()

    return city

async def get_all_cities(db: AsyncSession):
    stmt = select(models.City)
    result = await db.execute(stmt)
    cities = result.scalars().all()

    return cities
