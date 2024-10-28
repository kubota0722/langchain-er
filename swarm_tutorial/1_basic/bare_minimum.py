from swarm import Swarm, Agent

client = Swarm()

# basic agent settings
agent = Agent(
    name="Agent",
    instructions="You are a useful agent. You need to answer the user's question with japanese."
)

messages = [
    {"role": "user", "content": "Hello! How are you?"}
]
response = client.run(
    agent=agent,
    messages=messages,
)

print(response)
print(response.messages[-1]["content"])