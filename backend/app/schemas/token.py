from typing import Optional
from pydantic import BaseModel

# Schema für die Antwort beim Login
class Token(BaseModel):
    access_token: str
    token_type: str

# Inhalt des Tokens (Payload)
class TokenPayload(BaseModel):
    sub: Optional[int] = None
