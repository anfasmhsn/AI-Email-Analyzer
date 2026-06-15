from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

email = input("Enter Email: ")

score = analyzer.polarity_scores(email)

print(score)

if score['compound'] >= 0.05:
    print("Positive")

elif score['compound'] <= -0.05:
    print("Negative")

else:
    print("Neutral")