import bcrypt
from src.adapters.hash.hash_adapter_interface import PasswordHasherInterface

class BcryptPasswordHasher(PasswordHasherInterface):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()