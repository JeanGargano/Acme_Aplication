# Model/DocumentModel.py

from pydantic import BaseModel

class Document(BaseModel):
    content: str
    file_type: str
