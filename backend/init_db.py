import asyncio
from sqlalchemy import text
from app.db.session import engine

async def setup_database():
    async with engine.begin() as connection:
        with open("app/models/db.sql", "r") as f:
            sql = f.read()
        await connection.execute(text(sql))
    print("✅ Database tables initialized!")

if __name__ == "__main__":
    asyncio.run(setup_database())