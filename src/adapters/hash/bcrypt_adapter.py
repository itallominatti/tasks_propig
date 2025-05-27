import bcrypt
from src.adapters.hash.hash_adapter_interface import PasswordHasherInterface


class BcryptPasswordHasher(PasswordHasherInterface):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
