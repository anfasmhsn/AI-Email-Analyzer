import csv
import os

def save_email(email, category, sentiment, priority):

    file_exists = os.path.isfile("emails.csv")

    with open("emails.csv", "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "email",
                "category",
                "sentiment",
                "priority"
            ])

        writer.writerow([
            email,
            category,
            sentiment,
            priority
        ])