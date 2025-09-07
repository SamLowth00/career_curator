from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Dict, Any
from app.db import get_async_session
from app.auth.models import User
from app.auth.routes import current_active_user as get_current_active_user
from app.langchain.agent import CareerAgent

router = APIRouter()

# Store active agents per user (in production, use Redis or similar)
active_agents: Dict[str, CareerAgent] = {}

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[Dict[str, str]]
class ConversationHistory(BaseModel):
    conversation_history: List[Dict[str, str]]

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    chat_message: ChatMessage,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_active_user)
):
    """
    Chat with the career agent.
    
    This endpoint handles conversational interactions with the AI agent.
    The agent can help with job summaries.
    """ 
    try:
        user_id = str(user.id)
        if user_id not in active_agents:
            active_agents[user_id] = CareerAgent(db, user)

        agent = active_agents[user_id]

        response = await agent.chat(chat_message.message)
        # Get conversation history
        history = agent.get_conversation_history()

        return ChatResponse(
            response=response,
            conversation_history=history
        )
    except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error retrieving job summary: {str(e)}")
    

@router.get("/history", response_model=ConversationHistory)
async def get_conversation_history(
    user: User = Depends(get_current_active_user)
):
    """Get the conversation history for the current user"""
    try:
        user_id = str(user.id)
        if user_id not in active_agents:
            return ConversationHistory(conversation_history=[])
        
        agent = active_agents[user_id]

        history = agent.get_conversation_history()

        return ConversationHistory(conversation_history=history)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@router.post("/clear")
async def clear_conversation(
    user: User = Depends(get_current_active_user)
):
    """Clear the conversation history for the current user"""
    try:
        print('CLEARED CHAT');
        user_id = str(user.id)
        if user_id in active_agents:
            active_agents[user_id].clear_memory()
        
        return {"message": "Conversation history cleared"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")
    
@router.get("/debug")
async def debug_agent(
    user: User = Depends(get_current_active_user)
):
    """Get debug information about the agent (great for learning!)"""
    try:
        user_id = str(user.id)
        if user_id not in active_agents:
            return {"message": "No agent found for this user"}
        
        agent = active_agents[user_id]
        debug_info = agent.debug_info()
        
        return debug_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting debug info: {str(e)}")