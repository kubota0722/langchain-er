from swarm import Swarm, Agent

client = Swarm()


def transfer_to_spanish_agent():
    """return the spanish agent"""
    return spanish_agent

# setting AI agent of English speaker
english_agent = Agent(
    name="English Agent",
    instructions="You only speak English.",
    functions=[transfer_to_spanish_agent],
)

# setting AI agent of Spanish speaker
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish.",
)


# Add function to english agent
#english_agent.functions.append(transfer_to_spanish_agent)

# setting the message and executing the agent
messages = [
    {"role": "user", "content": "Hola. ¿Como estás?"}
]
response = client.run(agent=english_agent, messages=messages)

# print the response
print(response)