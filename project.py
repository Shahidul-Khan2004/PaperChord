from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random

def main():
    text = input("Enter your text: ")
    print(add_keywords_to_sentiment(analyze_sentiment(text)))

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

if __name__ == "__main__":
    main()