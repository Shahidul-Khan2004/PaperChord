from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
import requests

def main():
    text = input("Enter your text: ")
    print(fetch_suggestions(add_keywords_to_sentiment(analyze_sentiment(text))))

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
    songs = []
    response = requests.get(f"https://itunes.apple.com/search?term={str}&media=music&entity=song&limit=3")
    json = response.json()
    for result in json["results"]:
        songs.append(
            {
                "trackName": result["trackName"],
                "artistName": result["artistName"],
                "trackViewUrl": result["trackViewUrl"],
                "artworkUrl100": result["artworkUrl100"],
            }
        )
    return songs


if __name__ == "__main__":
    main()