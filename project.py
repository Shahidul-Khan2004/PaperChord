from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
    text = input("Enter your text: ")
    print(analyze_sentiment(text))

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score['compound'] >= 0.25:
        return "Positive"
    elif score['compound'] <= -0.25:
        return "Negative"
    else:
        return "Neutral"

if __name__ == "__main__":
    main()