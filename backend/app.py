from fastapi import FastAPI
from pydantic import BaseModel, Field
from project import fetch_suggestions, add_keywords_to_sentiment, analyze_sentiment

app = FastAPI(title="PaperChord API", version="1.0", description="An API to suggest songs based on the sentiment of input text.")
# an application instance of FastAPI is created

class SongRequest(BaseModel):
# a class of Pydantic's BaseModel is defined to validate the request body for song suggestions
    text: str = Field(..., example="I am feeling great today!", description= "Input text to analyze sentiment and fetch song suggestions.")
    limit: int | None = Field(None, ge=1, le=10, example=3, description= "Number of song suggestions to return (1-10). Default is 3.")

class SongResponse(BaseModel):
# a class of Pydantic's BaseModel is defined to validate the response body for song suggestions
    song: str
    artist: str
    url: str | None = None
    thumbnail: str | None = None

@app.get("/health", tags=["system"])
# app has a GET endpoint /health to check the health status of the API
def health_check():
# a function that executes when the /health endpoint is called
    return {"status": "ok"}

@app.post("/songs", response_model=list[SongResponse], response_model_exclude_none=True, tags=["suggestions"])
# app has a POST endpoint /songs to suggest songs based on input text sentiment
# the response model is a list of SongResponse objects, excluding any fields with None values
def suggest_songs(request: SongRequest):
# a function that executes when the /songs endpoint is called
    songs = fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(request.text)), request.limit or 3)
    return songs
