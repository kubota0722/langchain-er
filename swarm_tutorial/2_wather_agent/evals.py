from swarm import Swarm
from agents import weather_agent
import pytest

client = Swarm()

def run_and_get_tool_calls(agent, query):
    """Run a query through the agent and return any tool calls made.
    
    Args:
        agent: The agent to run the query through
        query: The query string to send to the agent
        
    Returns:
        list: A list of tool calls made by the agent during execution
    """
    messages = [{"role": "user", "content": query}]
    response = client.run(
        agent=agent,
        messages=[messages],
        execute_tools=False,
    )
    return response.messages[-1].get("tool_calls", [])

@pytest.mark.parametrize(
    "query",
    [
        "東京の天気は？",
        "大阪の天気を教えて",
        "今日傘が必要？福岡にいます",
    ]
)

def test_calls_weather_when_asked(query):
    """Test that the agent correctly calls the weather function when asked about weather.
    Tests that when asked about weather in Japanese, the agent properly calls the get_weather function."""
    tool_calls = run_and_get_tool_calls(weather_agent, query)

    assert len(tool_calls) == 1
    assert tool_calls[0]["function"]["name"] == "get_weather"


@pytest.mark.parametrize(
    "query",
    [
        "アメリカ合衆国の大統領はだれ？",
        "ドナルド・トランプは誰？",
        "バイデン大統領は誰？",
    ]
)

def test_does_not_call_weather_when_not_asked(query):
    """Test that the agent does not call the weather function when asked about other topics."""
    tool_calls = run_and_get_tool_calls(weather_agent, query)
    
    assert not tool_calls