from fastapi import FastAPI
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router

# Create FastAPI instance
app = FastAPI(title="PaperChord API", version="1.0.0")

# Include health check router
app.include_router(health_router)

# Include auth router
app.include_router(auth_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "PaperChord API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)