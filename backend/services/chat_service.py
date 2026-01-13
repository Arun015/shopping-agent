import uuid
from typing import Dict
from backend.agents import ShoppingAgentSession
from backend.services.safety_service import safety_service


class ChatService:
    def __init__(self):
        self.sessions: Dict[str, ShoppingAgentSession] = {}
    
    def get_or_create_session(self, session_id: str = None) -> tuple[str, ShoppingAgentSession]:
        if session_id and session_id in self.sessions:
            return session_id, self.sessions[session_id]
        
        new_session_id = session_id or str(uuid.uuid4())
        self.sessions[new_session_id] = ShoppingAgentSession()
        return new_session_id, self.sessions[new_session_id]
    
    def chat(self, message: str, session_id: str = None) -> tuple[str, str]:
        is_valid, error_msg = safety_service.validate_input(message)
        if not is_valid:
            return error_msg, session_id or str(uuid.uuid4())
        
        session_id, agent_session = self.get_or_create_session(session_id)
        
        try:
            response = agent_session.chat(message)
            return response, session_id
        except Exception as e:
            return f"I encountered an issue processing your request. Please try rephrasing your question.", session_id
    
    def clear_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]


chat_service = ChatService()



