import asyncpg
from app.core.config import settings

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        """Create the connection pool."""
        if not self.pool:
            print("Connecting to Supabase (Postgres)...")
            self.pool = await asyncpg.create_pool(
                dsn=settings.DATABASE_URL,
                min_size=1,
                max_size=10
            )
            print("Connected.")

    async def disconnect(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
            print("Disconnected.")

    async def fetch_one(self, query: str, *args):
        """Helper for SELECT single row."""
        if not self.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetch_all(self, query: str, *args):
        """Helper for SELECT multiple rows."""
        if not self.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query: str, *args):
        """Helper for INSERT/UPDATE/DELETE."""
        if not self.pool:
            raise RuntimeError("Database pool is not initialized.")
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

db = Database()