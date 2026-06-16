from classifier import classify_email
from sentiment import get_sentiment
from priority import get_priority

email = input("Enter Email: ")

category = classify_email(email)
sentiment = get_sentiment(email)

print("Category:", category)
print("Sentiment:", sentiment)
print("Priority:", get_priority(email, category))