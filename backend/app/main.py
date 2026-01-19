from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import db
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to DB
    await db.connect()
    yield
    # Shutdown: Disconnect DB
    await db.disconnect()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "PaperChord API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)