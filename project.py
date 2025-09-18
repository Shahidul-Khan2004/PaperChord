import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description="Get song suggestions based on text.")
    parser.add_argument("--text", type=str, help="Input text for song suggestions", required=True)
    parser.add_argument("--output", type=str, help="Output text for song suggestions")
    args = parser.parse_args()
    res = fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(args.text)))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False)
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))

def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of the given text and return 'Positive', 'Negative', or 'Neutral'."""
    try:
        analyzer = SentimentIntensityAnalyzer()
    except LookupError:
        import nltk
        nltk.download("vader_lexicon")
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
        response = requests.get(f"https://itunes.apple.com/search?term={str}&media=music&entity=song&limit=3", timeout=12)
        response.raise_for_status()
        json_response = response.json()
        for result in json_response["results"]:
            songs.append(
                {
                    "song": result.get("trackName", "N/A"),
                    "artist": result.get("artistName", "N/A"),
                    "url": result.get("trackViewUrl", None),
                    "thumbnail": result.get("artworkUrl100", None),
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