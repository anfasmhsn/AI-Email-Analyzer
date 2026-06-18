from classifier import classify_email
def get_sentiment(email: str) -> str:
    low = email.lower()
    positive_words = ("good", "great", "thanks", "thank", "happy", "appreciate", "congrat")
    negative_words = ("bad", "angry", "complaint", "sorry", "issue", "unhappy", "hate", "problem")

    pos = sum(1 for w in positive_words if w in low)
    neg = sum(1 for w in negative_words if w in low)

    if pos > neg:
        return "Positive"
    if neg > pos:
        return "Negative"
    return "Neutral"

from priority import get_priority
from save_email import save_email

email = input("Enter Email: ")

category = classify_email(email)
sentiment = get_sentiment(email)
priority = get_priority(email, category, sentiment)


save_email(
    email,
    category,
    sentiment,
    priority
)

print("Saved Successfully")
print("\nResults")
print("--------")
print("Category :", category)
print("Sentiment:", sentiment)
print("Priority :", priority)