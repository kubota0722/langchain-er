from swarm import Swarm, Agent

client = Swarm()

def instructions(context_variables):
    # obtain user-name from context variables and generate instructions
    name = context_variables.get("name", "user")
    return f"You are useful agent. Please greet user by name ({name})"

def print_account_details(context_variables: dict):
    # print account details
    user_id = context_variables.get("user_id", None)
    name    = context_variables.get("name"   , None)
    print(f"Account details: {name} {user_id}")
    return "success"

def update_account_details(context_variables: dict):
    # update account details (update account details to latest version)
    context_variables["name"] = "kk0722-latest"
    context_variables["user_id"] = "K0123456789-latest"
    return "success"

# setting the agent
agent = Agent(
    name="Agent",
    instructions=instructions,
    functions=[print_account_details, update_account_details],
)

# setting the context variables
context_variables = {
    "name"   : "kk0722",
    "user_id": "K0123456789",
}

"""
# excuting the first response
response = client.run(
    messages=[{"role": "user", "content": "こんにちは！"}],
    agent=agent,
    context_variables=context_variables,
)
# print the response
print(response.messages[-1]["content"])

# excuting output of the account details
response = client.run(
    messages=[{"role": "user", "content": "アカウント詳細を表示してください。"}],
    agent=agent,
    context_variables=context_variables,
)
# print the response
print(response.messages[-1]["content"])
"""

# update the account details
response = client.run(
    messages=[{"role": "user", "content": "アカウント詳細を最新化してください。"}],
    agent=agent,
    context_variables=context_variables,
)
# print the response
print(response.messages[-1]["content"])
print(context_variables)
print(response)
print(response.context_variables)