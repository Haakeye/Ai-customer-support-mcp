from llm_integration.agent import agent

def main():
    print("AI Customer Support Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = agent(user_input)
        print("AI:", response)


if __name__ == "__main__":
    main()