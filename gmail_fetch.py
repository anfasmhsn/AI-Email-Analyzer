from gmail_service import gmail_login
import base64

def fetch_emails(limit=5):

    service = gmail_login()

    results = service.users().messages().list(
        userId="me",
        maxResults=limit
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        subject = ""
        sender = ""
        body = ""

        headers = message["payload"]["headers"]

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]

            if header["name"] == "From":
                sender = header["value"]

        if "data" in message["payload"]["body"]:

            body = base64.urlsafe_b64decode(
                message["payload"]["body"]["data"]
            ).decode()

        emails.append({
            "from": sender,
            "subject": subject,
            "body": body
        })

    return emails