# Model/DocumentModel.py
from typing import Dict, Any
from pydantic import BaseModel

class Document(BaseModel):
    content: str
    file_type: str = "pdf"
    metadata: Dict[str, Any] = {}

class PromptDocumento(BaseModel):
    prompt: str
