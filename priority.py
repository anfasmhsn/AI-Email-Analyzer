def get_priority(email, category, sentiment=None):

    email = email.lower()

    score = 0

    # Category weights
    if category == "Complaint":
        score += 5

    elif category == "Resignation":
        score += 5

    elif category == "Payroll Issue":
        score += 4

    elif category == "Leave Request":
        score += 3

    elif category == "Recruitment":
        score += 2

    elif category == "Meeting":
        score += 2

    elif category == "Project Update":
        score += 2

    # Important keywords
    high_keywords = [
        "urgent",
        "immediately",
        "asap",
        "critical",
        "security",
        "alert",
        "password",
        "verify",
        "deadline",
        "payment failed",
        "failed",
        "invoice",
        "salary",
        "payroll"
    ]

    medium_keywords = [
        "meeting",
        "interview",
        "leave",
        "training",
        "promotion",
        "offer",
        "confirmation",
        "schedule"
    ]

    for word in high_keywords:
        if word in email:
            score += 3

    for word in medium_keywords:
        if word in email:
            score += 2

    # Sentiment
    if sentiment == "Negative":
        score += 1

    elif sentiment == "Positive":
        score -= 1

    # Final Priority
    if score >= 8:
        return "High"

    elif score >= 4:
        return "Medium"

    else:
        return "Low"