from typing import Optional
from pydantic import BaseModel, EmailStr

# Gemeinsame Eigenschaften für alle User-Schemas
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False

# Eigenschaften, die bei der Erstellung (Registrierung) benötigt werden
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Eigenschaften, die bei Updates geändert werden können
class UserUpdate(UserBase):
    password: Optional[str] = None

# Eigenschaften, die in der Datenbank gespeichert sind (für interne Nutzung)
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True

# Was an den Client zurückgegeben wird (OHNE Passwort!)
class User(UserInDBBase):
    pass

# Was in der DB gespeichert ist (MIT gehashtem Passwort)
class UserInDB(UserInDBBase):
    hashed_password: str
