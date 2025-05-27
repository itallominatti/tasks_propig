from abc import ABC, abstractmethod

class JWTAdapterInterface(ABC):
    @abstractmethod
    def encode(self, payload: dict) -> str:
        """
        Encodes a payload into a JWT token.
        
        :param payload: The data to encode in the JWT.
        :return: A JWT token as a string.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def decode(self, token: str) -> dict:
        """
        Decodes a JWT token back into its payload.
        
        :param token: The JWT token to decode.
        :return: The decoded payload as a dictionary.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")