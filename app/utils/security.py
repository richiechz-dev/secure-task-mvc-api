import secrets
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash # Libreria para el hash de contraseñas, moderna y como alternativa a passlib.

password_hash = PasswordHash.recommended() # Por debajo usa el algoritmo de hash moderno, que es argon2. Ya que es moderno y seguro Pero como alternativa esta tambien bycrypt. 

# Passwords - Hashing and Verification

# Funcion para hashear una contraeña
def hash_password(password: str) -> str:
    """Hash a password using argon2."""
    return password_hash.hash(password)
# Funcion para verificar una contraseña contra un hash
def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    try:
        return password_hash.verify(password, hashed_password)
    except Exception:
        return False

# Token Generation - Secure Random Tokens
def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length) # 'token_urlsafe' genera caracteres que no dan problemas en una URL o Header.

def generate_expiration_time(hours: int = 24) -> datetime:
    """Generate an expiration time for tokens."""
    return datetime.now(timezone.utc) + timedelta(hours=hours)

