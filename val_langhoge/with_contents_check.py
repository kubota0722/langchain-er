import asyncio
from langgraph.graph import StateGraph
from typing import TypedDict, List


# --- graphに流すstate ---
class TextState(TypedDict):
    text: str
    forbidden_words: List[str]
    next_action: str
    count: int
    is_changed: bool


# --- node内で使用する関数 ---
def _decide_next_action(state: TextState):
    print("decide next action")

    if any(word in state["text"] for word in state["forbidden_words"]):
        state["next_action"] = "delete"
    else:
        state["next_action"] = "finalize"
    return state


def _delete_forbidden_words(state: TextState):
    print("delete forbidden words")
    
    # 禁止用語を '*' に置き換える
    for word in state["forbidden_words"]:
        replacement = '*' * len(word)
        state["text"] = state["text"].replace(word, replacement)
    
    state["count"] += 1
    return state


def _finalize_all_actions(state: TextState):
    print("finalize all actions")

    if state["count"] >= 1:
        state["is_changed"] = True
    return state


def _routing_next_action(state: TextState):
    print("routing next action")

    return state["next_action"]


async def main():
    state = TextState(text="黒烏龍茶はとても美味しいです", forbidden_words=["黒烏龍茶"], next_action="", count=0, is_changed=True)

    # --- LangGraph ---
    workflow = StateGraph(TextState)

    # --- node ---
    workflow.add_node(
        "router",
        _decide_next_action
    )
    workflow.add_node(
        "delete",
        _delete_forbidden_words
    )
    workflow.add_node(
        "finalize",
        _finalize_all_actions
    )

    # --- edge ---
    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        _routing_next_action
    )
    workflow.add_edge(
        "delete",
        "router"
    )
    workflow.set_finish_point("finalize")

    # --- compile ---
    app = workflow.compile()

    # 初期状態を引数として渡す
    try:
        print(state)
        result = await app.ainvoke(state)
        print(result)
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    asyncio.run(main())
