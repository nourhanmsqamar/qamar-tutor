from sqlalchemy.orm import Session
from backend.app.models.document import Document
from backend.app.models.chat import ChatSession, Message

class ChatService:
    @staticmethod
    def create_document(db: Session, user_id: int, filename: str, original_filename: str) -> Document:
        new_document = Document(
            owner_id=user_id,
            filename=filename,
            original_filename=original_filename
        )
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        return new_document

    @staticmethod
    def get_or_create_session(db: Session, user_id: int, document_id: int) -> ChatSession:
        # In this implementation we will always create a new session for a new interaction,
        # or we could check if there is an active session. The prompt said "Create Chat Session (if new)".
        # For simplicity, if we don't have a session_id in the request, we create a new one.
        session = ChatSession(
            user_id=user_id,
            document_id=document_id,
            title=f"Chat for Document {document_id}"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def save_message(db: Session, session_id: int, role: str, content: str) -> Message:
        new_message = Message(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    @staticmethod
    def get_user_sessions(db: Session, user_id: int):
        from sqlalchemy.orm import joinedload
        sessions = db.query(ChatSession).options(
            joinedload(ChatSession.document),
            joinedload(ChatSession.messages)
        ).filter(ChatSession.user_id == user_id).all()
        
        result = []
        for s in sessions:
            last_msg = max((m.created_at for m in s.messages), default=None)
            result.append({
                "id": s.id,
                "title": s.title,
                "document_name": s.document.original_filename if s.document else "Unknown",
                "created_at": s.created_at,
                "last_message_at": last_msg
            })
        return result

    @staticmethod
    def get_session_messages(db: Session, session_id: int, user_id: int):
        from fastapi import HTTPException
        session = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == user_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or not owned by user")
        
        messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.asc()).all()
        return messages

    @staticmethod
    def delete_session(db: Session, session_id: int, user_id: int):
        from fastapi import HTTPException
        session = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == user_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or not owned by user")
        
        db.delete(session)
        db.commit()
        return True

    @staticmethod
    def rename_session(db: Session, session_id: int, user_id: int, new_title: str):
        from fastapi import HTTPException
        session = db.query(ChatSession).filter(ChatSession.id == session_id, ChatSession.user_id == user_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found or not owned by user")
        
        session.title = new_title
        db.commit()
        db.refresh(session)
        return session

chat_service = ChatService()
