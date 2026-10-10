from chatbot.chat import ask_chatbot


def main():
    print("SmartMail AI Chatbot")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("SmartMail AI: Goodbye!")
            break

        if not question:
            continue

        try:
            answer = ask_chatbot(question)
            print("\nSmartMail AI:", answer)
        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()