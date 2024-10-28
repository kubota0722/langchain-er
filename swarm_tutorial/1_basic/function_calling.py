from swarm import Swarm, Agent

client = Swarm()

def get_wether_in_japan(location: str)-> str:
    match location:
        case "Tokyo":
            weather = "sunny"
        case "Nagano":
            weather = "rainy"
        case "Osaka":
            weather = "cloudy"
        case "Hokkaido":
            weather = "snow"
        case _ :
            weather = "I don't know"
    return weather


def get_weather_in_NewYork(location: str)-> str:
    # return dummy weather data
    return "{'temp':67, 'unit':'F'}"

agent = Agent(
    name="Agent",
    instructions="You are a helpful AI agent.",
    functions=[get_weather_in_NewYork, get_wether_in_japan],
)

messages = [{"role": "user", "content": "東京（Tokyo）の天気を教えてください"}]

response = client.run(agent=agent, messages=messages)

print(response)