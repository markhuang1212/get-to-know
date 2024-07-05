from typing import Annotated, Literal, Sequence, TypedDict

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.checkpoint import MemorySaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    messages: Annotated[list, add_messages]


def should_continue(state: State) -> Literal["tools", "__end__"]:
    """Return the next node to execute."""
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "__end__"
    return "tools"


class ModelNode():
    model: BaseChatModel

    def __init__(self, model: BaseChatModel):
        self.model = model

    def __call__(self, state: dict):
        response = self.model.invoke(state["messages"])
        return {"messages": [response]}


def create_knowledge_agent(model: BaseChatModel, tools: Sequence[BaseTool]):
    tool_node = ToolNode(tools)

    workflow = StateGraph(State)
    workflow.add_node("agent", ModelNode(model))
    workflow.add_node("tools", tool_node)
    workflow.set_entry_point("agent")

    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent")

    return workflow.compile()
