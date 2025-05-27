from datetime import datetime, timedelta
import jwt

from src.adapters.jwt.jwt_adapter_interface import JWTAdapterInterface

class JWTAdapter(JWTAdapterInterface):
    def __init__(self, secret_key: str, algorithm: str = 'HS256', expiration_minutes: int = 60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration_minutes = expiration_minutes

    def encode(self, payload: dict) -> str:
        if 'exp' not in payload:
            payload['exp'] = datetime.utcnow() + timedelta(minutes=self.expiration_minutes)
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")