import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
import requests
import argparse

def main():
    """
    Parses command-line arguments, analyzes the sentiment of input text,
    fetches song suggestions based on sentiment, and outputs the results.

    Returns
    -------
    None
    """
    parser = argparse.ArgumentParser(description="Get song suggestions based on text.")
    parser.add_argument("--text", type=str, help="Input text for song suggestions", required=True)
    parser.add_argument("--output", type=str, help="Output text for song suggestions")
    parser.add_argument("--limit", type=int, help="Number of songs to get")
    args = parser.parse_args()
    if args.limit and args.limit > 0:
        res = fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(args.text)), args.limit)
    else:
        res = fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(args.text)))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False)
    else:
        print(json.dumps(res, indent=2, ensure_ascii=False))

def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of the given text and return a sentiment label.

    Parameters
    ----------
    text : str
        The input text to analyze.

    Returns
    -------
    str
        'Positive', 'Negative', or 'Neutral' based on sentiment analysis.
    """
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
    """
    Assign a random keyword based on the relevant sentiment.

    Parameters
    ----------
    sentiment : str
        The sentiment label ('Positive', 'Negative', or 'Neutral').

    Returns
    -------
    str
        A keyword associated with the provided sentiment.
    """
    if sentiment == "Positive":
        return random.choice(["good mood", "happy", "chill vibes", "feel good", "relaxing"])
    elif sentiment == "Negative":
        return random.choice(["sad song", "blue", "heart break", "memories"])
    else:
        return random.choice(["inspo", "lofi", "nature", "mood", "calm"])

def fetch_suggestions(keyword: str, limit : int = 3) -> list:
    """
    Fetch song suggestions from the iTunes API based on the given keyword.

    Parameters
    ----------
    keyword : str
        Keyword to search for songs on the iTunes API.
    limit : int, optional
        The maximum number of song suggestions to return (default is 3).

    Returns
    -------
    list of dict
        A list of dictionaries, each containing information about a song (song name, artist, url, thumbnail).
    """
    try:
        songs = []
        params = {
            "term": keyword,
            "media": "music",
            "entity": "song",
            "limit": limit,
        }
        response = requests.get("https://itunes.apple.com/search", params=params, timeout=12)
        response.raise_for_status()
        json_response = response.json()
        for result in json_response.get("results", []):
            songs.append(
                {
                    "song": result.get("trackName", "N/A"),
                    "artist": result.get("artistName", "N/A"),
                    "url": result.get("trackViewUrl", None),
                    "thumbnail": result.get("artworkUrl100", None),
                }
            )
        return songs[:limit]
    except requests.RequestException as e:
        print(f"Itunes not responding: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

if __name__ == "__main__":
    main()