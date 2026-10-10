from chatbot.vector_store import get_retriever
from chatbot.prompt import SYSTEM_PROMPT


def get_email_context(question):
    """Retrieve relevant emails from the vector database."""

    retriever = get_retriever()
    documents = retriever.invoke(question)

    if not documents:
        return ""

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    return context


def ask_chatbot(question):
    """Answer a question using retrieved email information."""

    context = get_email_context(question)

    if not context:
        return "I couldn't find relevant information in your emails."

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    # Temporary: display retrieved context until we connect an LLM.
    return (
        "Relevant email information retrieved successfully:\n\n"
        + context
    )