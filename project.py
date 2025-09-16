from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

text = input("Enter your text: ")

score = analyzer.polarity_scores(text)

print("Sentiment Score:", score["compound"])