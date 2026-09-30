from gmail_service import gmail_login
import base64


def get_body(payload):

    body = ""

    # Simple email
    if "body" in payload and payload["body"].get("data"):
        body = base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode("utf-8", errors="ignore")

    # Multipart email
    elif "parts" in payload:

        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                data = part.get("body", {}).get("data")

                if data:
                    body = base64.urlsafe_b64decode(
                        data
                    ).decode(
                        "utf-8",
                        errors="ignore"
                    )

                    break

            elif "parts" in part:

                body = get_body(part)

                if body:
                    break

    return body


def fetch_emails(limit=20):

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
        date = ""

        headers = message["payload"].get(
            "headers",
            []
        )

        for header in headers:

            name = header["name"].lower()

            if name == "subject":
                subject = header["value"]

            elif name == "from":
                sender = header["value"]

            elif name == "date":
                date = header["value"]

        # -----------------------------------------
        # GMAIL LABELS
        # -----------------------------------------

        labels = message.get(
            "labelIds",
            []
        )

        emails.append({

            # Gmail unique message ID
            "gmail_id": msg["id"],

            "sender": sender,

            "subject": subject,

            "body": get_body(
                message["payload"]
            ),

            "date": date,

            # Gmail labels
            "labels": labels
        })

    return emails