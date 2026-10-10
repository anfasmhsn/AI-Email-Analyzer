from chatbot.vector_store import get_retriever


def search_emails(question):
    retriever = get_retriever()

    documents = retriever.invoke(question)

    if not documents:
        print("No relevant emails found.")
        return

    print("\n========== SEARCH RESULTS ==========\n")

    for i, document in enumerate(documents, start=1):

        print(f"----- Email {i} -----")

        print("Sender:", document.metadata.get("sender"))
        print("Subject:", document.metadata.get("subject"))
        print("Category:", document.metadata.get("category"))
        print("Sentiment:", document.metadata.get("sentiment"))
        print("Priority:", document.metadata.get("priority"))

        print("\nContent:")
        print(document.page_content[:1000])

        print("\n")


if __name__ == "__main__":

    question = input("Ask about your emails: ")

    search_emails(question)