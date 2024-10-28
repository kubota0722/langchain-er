from swarm import Swarm, Agent

client = Swarm()

# setting agent
my_agent = Agent(
    name="Agent",
    instructions="You are a helpful AI agent.",
)

def pretty_print_messages(messages):
    # print messages
    for message in messages:
        if message["content"] is None:
            continue
        print(f"{message['sender']}: {message['content']}")

messages = []
agent = my_agent

while True:
    user_input = input("> ")
    messages.append({"role": "user", "content": user_input})

    response = client.run(agent=agent, messages=messages)
    messages = response.messages
    agent = response.agent

    pretty_print_messages(messages)