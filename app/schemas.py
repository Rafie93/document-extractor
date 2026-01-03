from pydantic import BaseModel
from typing import List

class ExtractRequest(BaseModel):
    file_url: str
    document_id: int
    file_type: str  # pdf | excel

class Chunk(BaseModel):
    page: int
    content: str

class ExtractResponse(BaseModel):
    document_id: int
    chunks: List[Chunk]
