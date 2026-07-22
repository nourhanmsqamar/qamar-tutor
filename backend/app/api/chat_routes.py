from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.core.security import get_current_user
from backend.app.services.chat_service import chat_service
from backend.app.schemas.chat import SessionResponse, MessageResponse, RenameSessionRequest

router = APIRouter(
    prefix="/chat/sessions",
    tags=["Chat Management"]
)

@router.get("", response_model=List[SessionResponse])
def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = chat_service.get_user_sessions(db, current_user.id)
    return sessions

@router.get("/{session_id}", response_model=List[MessageResponse])
def get_session_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    messages = chat_service.get_session_messages(db, session_id, current_user.id)
    return messages

@router.delete("/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_service.delete_session(db, session_id, current_user.id)
    return {"status": "success", "message": "Session deleted successfully"}

@router.patch("/{session_id}")
def rename_session(
    session_id: int,
    request: RenameSessionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat_service.rename_session(db, session_id, current_user.id, request.title)
    return {"status": "success", "message": "Session renamed successfully"}
