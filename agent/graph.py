from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langchain_openai import ChatOpenAI

from typing import Annotated, TypedDict

from agent.tools.analytics_agent import analytics_agent
from agent.tools.project_agent import project_agent
from agent.tools.budget_agent import budget_agent

from utils.logging import log_msg_to_file

import datetime
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

class Agent:
    _instance = None  # Class-level attribute to store singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Agent, cls).__new__(cls)
        return cls._instance

    def __init__(self, llm, tools):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.llm = llm
        self.tools = tools
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.graph = self.init_graph()
    
    def init_graph(self):
        graph_builder = StateGraph(State)
        tool_node = ToolNode(self.tools)

        graph_builder.add_node("chatbot", self.chatbot)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition)
        graph_builder.add_edge("tools", "chatbot")
        graph_builder.add_edge(START, "chatbot")
        graph = graph_builder.compile()
        return graph

    def chatbot(self, state: State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}        

    def get_bot_response(self, message, history):
        LOG = {'user_msg': message, 'timestamp': str(datetime.datetime.now(datetime.timezone.utc)), 'tool_calls': []}
        
        messages = []
        if history:
            for human_msg, ai_msg in history:
                messages.append(HumanMessage(human_msg))
                messages.append(AIMessage(ai_msg))
        messages.append(HumanMessage(message))
        response = self.graph.invoke({'messages': messages})
        
        LOG['final_answer'] = response['messages'][-1].content

        log_msg_to_file(LOG)

        return response['messages'][-1].content
    
    async def stream_bot_response(self, message: str, history: list[tuple[str, str]]):
        LOG = {'user_msg': message, 'timestamp': str(datetime.datetime.now(datetime.timezone.utc)), 'tool_calls': []}

        final_answer = ""

        messages = []
        if history:
            for human_msg, ai_msg in history:
                messages.append(HumanMessage(human_msg))
                messages.append(AIMessage(ai_msg))
        messages.append(HumanMessage(message))

        for msg_chunk, metadata in self.graph.stream({'messages': messages}, stream_mode="messages"):
            if msg_chunk.content:
                if hasattr(msg_chunk, 'tool_call_id'):
                    tool_call_msg = f"Tool Called: {msg_chunk.name}, Results Returned: {msg_chunk.content}\n"
                    LOG['tool_calls'].append(tool_call_msg)
                    event = {'event': 'tool_call', 'content': tool_call_msg}
                    #yield tool_call_msg
                else:
                    final_answer += msg_chunk.content
                    event = {'event':'message', 'content': msg_chunk.content}
                    #yield msg_chunk.content
                yield event

        LOG['final_answer'] = final_answer

        log_msg_to_file(LOG)

    


def get_agent():
    llm = ChatOpenAI()
    tools = [analytics_agent,project_agent,budget_agent]
    a = Agent(llm=llm, tools=tools)
    return a
