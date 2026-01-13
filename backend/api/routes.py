from fastapi import APIRouter, HTTPException
from backend.dto import ChatRequest, ChatResponse, PhoneDTO
from backend.services import chat_service
from backend.dao import phone_dao
from typing import List

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response, session_id = chat_service.chat(request.message, request.session_id)
    return ChatResponse(
        response=response,
        session_id=session_id
    )


@router.get("/phones", response_model=List[PhoneDTO])
async def get_phones():
    try:
        phones = phone_dao.get_all()
        return phones
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/phones/{phone_id}", response_model=PhoneDTO)
async def get_phone(phone_id: int):
    try:
        phone = phone_dao.get_by_id(phone_id)
        if not phone:
            raise HTTPException(status_code=404, detail="Phone not found")
        return phone
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
