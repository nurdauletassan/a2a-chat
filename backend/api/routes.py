from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from assistant.a2a import A2AInteraction
from database.session import get_db
from database.models import Dialog, Message
import uuid
from typing import List, Optional
from datetime import datetime

router = APIRouter()
a2a = A2AInteraction()

class PromptRequest(BaseModel):
    prompt: str
    dialog_id: Optional[str] = None

class A2AResponse(BaseModel):
    response: str
    gemini_response: str
    openai_response: str
    dialog_id: str

class MessageResponse(BaseModel):
    id: int
    dialog_id: str
    prompt: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True

class DialogResponse(BaseModel):
    id: str
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]

    class Config:
        from_attributes = True

class DialogTitleUpdate(BaseModel):
    title: str

@router.post("/a2a", response_model=A2AResponse)
async def a2a_interaction(request: PromptRequest, db: Session = Depends(get_db)):
    try:
        # Generate or use existing dialog_id
        dialog_id = request.dialog_id or str(uuid.uuid4())
        
        # Get or create dialog
        dialog = db.query(Dialog).filter(Dialog.id == dialog_id).first()
        if not dialog:
            dialog = Dialog(id=dialog_id)
            db.add(dialog)
            db.commit()
        
        # Get response from A2A
        response = await a2a.interact(request.prompt)
        
        # Store message in database
        message = Message(
            dialog_id=dialog_id,
            prompt=request.prompt,
            response=response
        )
        db.add(message)
        db.commit()
        
        return A2AResponse(
            response=response,
            gemini_response=a2a.last_gemini_response,
            openai_response=a2a.last_openai_response,
            dialog_id=dialog_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dialogs", response_model=List[DialogResponse])
def get_dialogs(db: Session = Depends(get_db)):
    """Get list of all dialogs with their messages."""
    try:
        dialogs = db.query(Dialog).order_by(Dialog.updated_at.desc()).all()
        return dialogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dialogs/{dialog_id}", response_model=DialogResponse)
def get_dialog(dialog_id: str, db: Session = Depends(get_db)):
    """Get a specific dialog with its messages."""
    try:
        dialog = db.query(Dialog).filter(Dialog.id == dialog_id).first()
        if not dialog:
            raise HTTPException(status_code=404, detail="Dialog not found")
        return dialog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/dialogs/{dialog_id}")
def delete_dialog(dialog_id: str, db: Session = Depends(get_db)):
    """Delete a dialog and all its messages."""
    try:
        dialog = db.query(Dialog).filter(Dialog.id == dialog_id).first()
        if not dialog:
            raise HTTPException(status_code=404, detail="Dialog not found")
        
        db.delete(dialog)
        db.commit()
        return {"message": "Dialog deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/dialogs/{dialog_id}")
def update_dialog_title(dialog_id: str, title_update: DialogTitleUpdate, db: Session = Depends(get_db)):
    """Update dialog title."""
    try:
        dialog = db.query(Dialog).filter(Dialog.id == dialog_id).first()
        if not dialog:
            raise HTTPException(status_code=404, detail="Dialog not found")
        
        dialog.title = title_update.title
        db.commit()
        return {"message": "Dialog title updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 