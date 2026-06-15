def classify_email(email):
    email = email.lower()

    if "complaint" in email:
        return "Complaint"

    elif "leave" in email:
        return "Leave Request"

    elif "resign" in email:
        return "Resignation"

    elif "salary" in email:
        return "Payroll Issue"

    elif "interview" in email:
        return "Recruitment"

    else:
        return "General Inquiry"


def get_priority(email, category):
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

    if score >= 8:
        return "High"

    elif score >= 4:
        return "Medium"

    else:
        return "Low"


email = input("Enter your email: ")

category = classify_email(email)
priority = get_priority(email, category)

print("Category:", category)
print("Priority:", priority)