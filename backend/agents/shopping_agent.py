from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from backend.config import settings
from backend.agents.tools import tools


SYSTEM_PROMPT = """You are a helpful shopping assistant for mobile phones in the Indian market. Help users find phones based on their budget and needs.

Use the available tools to search phones, compare models, and explain technical terms. Always use real data from tools - never make up specifications.

When users ask to compare or explain technical terms, use the explain_technical_term tool. The tool can handle both single terms and comparisons (pass "term1 vs term2" for comparisons).

Only help with mobile phone queries. For other topics, politely decline. Stay neutral and factual about all brands.

When recommending phones, explain why they fit the user's requirements. For comparisons, highlight key differences and trade-offs."""


def create_shopping_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.3,
        google_api_key=settings.google_api_key
    )
    
    # Bind tools to the model
    llm_with_tools = llm.bind_tools(tools)
    
    return llm_with_tools


class ShoppingAgentSession:
    def __init__(self):
        self.llm = create_shopping_agent()
        self.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]
        self.tools_dict = {tool.name: tool for tool in tools}
    
    def chat(self, message: str) -> str:
        # Add user message
        self.chat_history.append(HumanMessage(content=message))
        
        # Get response from model
        response = self.llm.invoke(self.chat_history)
        
        # Handle tool calls
        max_iterations = 3
        iteration = 0
        
        while response.tool_calls and iteration < max_iterations:
            iteration += 1
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                if tool_name in self.tools_dict:
                    tool_result = self.tools_dict[tool_name].invoke(tool_args)
                    
                    # Add tool result to history
                    self.chat_history.append(AIMessage(
                        content="",
                        tool_calls=[tool_call]
                    ))
                    self.chat_history.append(HumanMessage(
                        content=f"Tool result: {tool_result}"
                    ))
            
            # Get next response
            response = self.llm.invoke(self.chat_history)
        
        # Extract final response text
        if hasattr(response, 'content'):
            if isinstance(response.content, list):
                # Extract text from list of content blocks
                final_content = " ".join([
                    block.get('text', '') if isinstance(block, dict) else str(block)
                    for block in response.content
                ])
            else:
                final_content = response.content
        else:
            final_content = str(response)
        
        self.chat_history.append(AIMessage(content=final_content))
        
        # Keep only last 10 messages (plus system message)
        if len(self.chat_history) > 11:
            self.chat_history = [self.chat_history[0]] + self.chat_history[-10:]
        
        return final_content
