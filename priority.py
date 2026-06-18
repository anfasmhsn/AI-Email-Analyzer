def get_priority(email, category, sentiment=None):
    score = 0

    if category == "Complaint":
        score += 5

    if category == "Resignation":
        score += 5

    if category == "Payroll Issue":
        score += 4

    if "urgent" in email.lower():
        score += 3

    if "deadline" in email.lower():
        score += 2

    # small boost for negative sentiment
    if sentiment == "Negative":
        score += 1

    if score >= 8:
        return "High"

    elif score >= 4:
        return "Medium"

    else:
        return "Low"