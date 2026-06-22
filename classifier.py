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