import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
import requests

def main():
    text = input("Enter your text: ")
    res = fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(text)))
    print(json.dumps(res, indent=2, ensure_ascii=False))

def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of the given text and return 'Positive', 'Negative', or 'Neutral'."""
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score["compound"] >= 0.25:
        return "Positive"
    elif score["compound"] <= -0.25:
        return "Negative"
    else:
        return "Neutral"

def add_keywords_to_sentiment(sentiment: str) -> str:
    """Assign a random keyword based on the relevant sentiment."""
    if sentiment == "Positive":
        return random.choice(["good mood", "happy", "chill vibes", "feel good", "relaxing"])
    elif sentiment == "Negative":
        return random.choice(["sad song", "blue", "heart break", "memories"])
    else:
        return random.choice(["inspo", "lofi", "nature", "mood", "calm"])

def fetch_suggestions(str: str) -> list:
    """Fetch song suggestions from the iTunes API based on the given keyword."""
    try:
        songs = []
        response = requests.get(f"https://itunes.apple.com/search?term={str}&media=music&entity=song&limit=3")

        json = response.json()
        for result in json["results"]:
            songs.append(
                {
                    "song": result["trackName"],
                    "artist": result["artistName"],
                    "url": result["trackViewUrl"],
                    "thumbnail": result["artworkUrl100"],
                }
            )
        return songs
    except requests.RequestException as e:
        print(f"Itunes not responding: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


if __name__ == "__main__":
    main()