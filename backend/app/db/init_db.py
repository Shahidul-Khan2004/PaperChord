import asyncio
import os
from app.db.session import db

async def init_db():
    await db.connect()
    
    # We use os.path.join to be safe across operating systems
    file_path = os.path.join(os.path.dirname(__file__), "init_db.sql")
    with open(file_path, "r") as f:
        sql_commands = f.read()
    
    print("Creating tables...")
    await db.execute(sql_commands)
    print("Tables created successfully.")
    
    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(init_db())