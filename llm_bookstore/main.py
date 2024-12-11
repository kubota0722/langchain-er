import asyncio
from langgraph.graph import StateGraph
from typing import TypedDict, Optional, List, Dict, Any

AGENT_SEARCH_COUNT_LIMIT = 3


class AgentState(TypedDict):
    user_input: str
    is_needed_more_info: bool
    search_count: int
    librarian_agent_result: Optional[Dict[str, Any]]


def librarian_agent(state: AgentState):
    #ここでは資料のid、名前、説明から、
    #探す必要があるかないか、また探すべき資料のidとそれに対する指示を渡す
    #また、3回検索しても満足できなかった場合は流石にやめる
    print("librarian_agent")
    if state["search_count"] < AGENT_SEARCH_COUNT_LIMIT:
        state["is_needed_more_info"] = True
    else:
        state["is_needed_more_info"] = False
    return state


def expert_agent(state: AgentState):
    #資料のidと指示を受け取り、推論をする
    #forでidごと回す？でもdict型だからどうすればいい
    
    print("expert_agent")
    state["search_count"] += 1
    return state




def final_agent(state: AgentState):
    print("final_agent")
    return state

def _routing_next_action(state: AgentState):
    if state["is_needed_more_info"] is True:
        return "expert_agent"
    else:
        return "final_agent"




async def main():
    user_input = ""

    state = AgentState(user_input=user_input, is_needed_more_info=False, search_count=0)
    workflow = StateGraph(AgentState)


    workflow.add_node("librarian_agent", librarian_agent)
    workflow.add_node("expert_agent", expert_agent)
    workflow.add_node("final_agent", final_agent)

    workflow.add_edge("expert_agent", "librarian_agent")
    workflow.set_entry_point("librarian_agent")
    workflow.add_conditional_edges("librarian_agent", _routing_next_action)
    workflow.set_finish_point("final_agent")

    app = workflow.compile()

    try:
        result = await app.ainvoke(state)
        print(result)
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    asyncio.run(main())
