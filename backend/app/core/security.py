from passlib.context import CryptContext

# Konfiguration des Passwort-Hashing-Algorithmus (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Überprüft, ob das eingegebene Passwort mit dem Hash übereinstimmt.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Erstellt einen Hash aus dem Passwort.
    """
    return pwd_context.hash(password)
