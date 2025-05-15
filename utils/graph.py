from typing import Annotated, TypedDict


from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage

from langchain_openai import ChatOpenAI

from tools.tools import analytics_agent, project_agent

import datetime
import os
import json
class State(TypedDict):
    messages: Annotated[list, add_messages]


class Agent:
    _instance = None  # Class-level attribute to store singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Agent, cls).__new__(cls)
        return cls._instance

    def __init__(self, llm, tools):
        # Optional: prevent reinitialization
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
        messages = []
        if history:
            for human_msg, ai_msg in history:
                messages.append(HumanMessage(human_msg))
                messages.append(AIMessage(ai_msg))
        messages.append(HumanMessage(message))
        response = self.graph.invoke({'messages': messages})

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
                    yield tool_call_msg
                else:
                    final_answer += msg_chunk.content
                    yield msg_chunk.content
        LOG['final_answer'] = final_answer
        self.log_msg_to_file(LOG)

    def log_msg_to_file(self, log):
        today = str(datetime.date.today())
        fpath = f'./logs/{today}.json'
        if not os.path.exists(fpath):
            with open(fpath, 'w') as f:
                json.dump([log], f, indent=2)
        else:
            with open(fpath, 'r') as f:
                logs = json.load(f)
            logs.append(log)
            with open(fpath, 'w') as f:
                json.dump(logs, f, indent=2)

        

OPENAI_API_KEY='keyhere'
llm = ChatOpenAI(api_key=OPENAI_API_KEY)
tools = [analytics_agent,project_agent]
a = Agent(llm=llm, tools=tools)
def test():
    OPENAI_API_KEY="keyhere"



    llm = ChatOpenAI()
    a = Agent(llm, None)
    msg = {
        'messages': []
    }
    x = input()
    while x != 'q':
        msg["messages"].append(HumanMessage(content=x))
        msg = a.graph.invoke(msg)
        print(msg)
        x = input()
