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

chat_service = ChatService()
