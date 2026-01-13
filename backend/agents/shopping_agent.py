from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from backend.config import settings
from backend.agents.tools import tools


SYSTEM_PROMPT = """You are a helpful shopping assistant for mobile phones in the Indian market. Help users find phones based on their budget and needs.

Use the available tools to search phones, compare models, and explain technical terms. Always use real data from tools - never make up specifications.

Only help with mobile phone queries. For other topics, politely decline. Stay neutral and factual about all brands.

When recommending phones, explain why they fit the user's requirements. For comparisons, highlight key differences and trade-offs."""


def create_shopping_agent():
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash-lite",
        temperature=0.3,
        google_api_key=settings.google_api_key
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3,
        handle_parsing_errors=True,
        return_intermediate_steps=False
    )
    
    return agent_executor


class ShoppingAgentSession:
    def __init__(self):
        self.agent = create_shopping_agent()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            max_token_limit=2000
        )
    
    def chat(self, message: str) -> str:
        chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
        
        response = self.agent.invoke({
            "input": message,
            "chat_history": chat_history
        })
        
        self.memory.save_context(
            {"input": message},
            {"output": response["output"]}
        )
        
        return response["output"]


