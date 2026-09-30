from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_chroma import Chroma

from database import get_emails
from chatbot.embeddings import get_embeddings


CHROMA_PATH = "data/email_chroma"


def clean_email_body(body):
    """Convert HTML email body into clean readable text."""

    if not body:
        return ""

    soup = BeautifulSoup(body, "html.parser")

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text


def create_documents():

    emails = get_emails()

    documents = []

    for email in emails:

        (
            email_id,
            gmail_id,
            sender,
            subject,
            body,
            category,
            sentiment,
            priority,
            date,
            labels
        ) = email

        clean_body = clean_email_body(body)

        content = f"""
Sender: {sender}

Subject: {subject}

Category: {category}

Sentiment: {sentiment}

Priority: {priority}

Date: {date}

Labels: {labels}

Email Body:
{clean_body}
"""

        document = Document(
            page_content=content,
            metadata={
                "email_id": email_id,
                "gmail_id": gmail_id or "",
                "sender": sender or "",
                "subject": subject or "",
                "category": category or "",
                "sentiment": sentiment or "",
                "priority": priority or "",
                "date": date or "",
                "labels": labels or "",
            }
        )

        documents.append(document)

    return documents


def create_vector_store():

    embeddings = get_embeddings()

    documents = create_documents()

    if not documents:
        raise ValueError("No emails found in the database.")

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    return vector_store


def get_retriever():

    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vector_store.as_retriever(
        search_kwargs={
            "k": 5
        }
    )