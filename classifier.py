
def classify_email(email):
    email=email.lower()
    score = 0
    if "complaint" in email:
        return "Complaint"
    elif "leave" in email:
        return "Leave request"
    elif "resign" in email:
        return "Resignation"
    elif "salary" in email:
        return "Payroll issue"
    elif "interview" in email:
        return "Recruitment"
    else:
        return "General inquiry"

email = input("Enter your email:")
result = classify_email(email)
print("Category:", result)