from fastapi import FastAPI
from pydantic import BaseModel, Field
from project import fetch_suggestions, add_keywords_to_sentiment, analyze_sentiment

app = FastAPI()

class SongRequest(BaseModel):
    text: str = Field(..., example="I am feeling great today!", description= "Input text to analyze sentiment and fetch song suggestions.")
    limit: int | None = Field(None, ge=1, le=10, example=3, description= "Number of song suggestions to return (1-10). Default is 3.")

class SongResponse(BaseModel):
    song: str
    artist: str
    url: str | None = None
    thumbnail: str | None = None

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}

@app.post("/songs", response_model=list[SongResponse], response_model_exclude_none=True, tags=["suggestions"])
def suggest_songs(request: SongRequest):
    songs = fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(request.text)), request.limit or 3)
    return songs
