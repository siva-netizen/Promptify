from modelConfig import GEMINI
def testModelConnection():
    print("Hello from promtify!")
    agent_response = GEMINI.invoke([
        {"role": "user", "content": "Hello, how are you?"}
    ])
    print("Agent response:", agent_response)


if __name__ == "__main__":
    testModelConnection()
