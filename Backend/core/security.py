import bcrypt
from passlib.context import CryptContext

# Maintain context for app-wide compatibility, though we bypass its hash logic
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Direct Bcrypt Implementation: 
    Bypasses passlib's internal 'AttributeError' and 'ValueError' bugs 
    on modern Python 3.14 environments.
    """
    # 1. Convert string to UTF-8 bytes
    # 2. Truncate to 72 bytes (Bcrypt's native limit)
    password_bytes = password.encode('utf-8')[:72]
    
    # 3. Generate a fresh salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # 4. Decode to string for storage in the PostgreSQL 'hashed_password' column
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a login attempt by comparing the plain text password 
    against the stored database hash.
    """
    # Convert incoming plain password to bytes and truncate
    password_bytes = plain_password.encode('utf-8')[:72]
    
    # The stored hash from DB must be encoded back to bytes for the comparison
    stored_hash_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, stored_hash_bytes)