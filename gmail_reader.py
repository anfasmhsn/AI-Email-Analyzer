from gmail_service import gmail_login
import base64

service = gmail_login()

results = service.users().messages().list(
    userId="me",
    maxResults=5
).execute()

messages = results.get("messages", [])

for msg in messages:

    message = service.users().messages().get(
        userId="me",
        id=msg["id"],
        format="full"
    ).execute()

    headers = message["payload"]["headers"]

    subject = ""
    sender = ""
    date = ""

    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]

        if header["name"] == "From":
            sender = header["value"]

        if header["name"] == "Date":
            date = header["value"]

    body = ""

    if "parts" in message["payload"]:

        for part in message["payload"]["parts"]:

            if part["mimeType"] == "text/plain":

                data = part["body"]["data"]

                body = base64.urlsafe_b64decode(
                    data
                ).decode("utf-8")

                break

    elif "data" in message["payload"]["body"]:

        data = message["payload"]["body"]["data"]

        body = base64.urlsafe_b64decode(
            data
        ).decode("utf-8")

    print("=" * 60)
    print("FROM    :", sender)
    print("SUBJECT :", subject)
    print("DATE    :", date)
    print("BODY")
    print(body[:500])