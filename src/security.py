from secrets import token_urlsafe
from hashlib import sha256
from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet

from src.config import settings


class Security:
    def __init__(self):
        key_bytes = settings.SECRET_KEY.encode("utf-8")
        key_digest = sha256(key_bytes).digest()
        fernet_key = urlsafe_b64encode(key_digest)
        self._fernet = Fernet(fernet_key)

    def create_secret_key(self) -> str:
        return token_urlsafe(32)

    def encrypt(self, secret_data: str) -> str:
        return self._fernet.encrypt(secret_data.encode("utf-8")).decode("utf-8")

    def decrypt(self, encrypted_data: str) -> str:
        return self._fernet.decrypt(encrypted_data.encode("utf-8")).decode("utf-8")


security_instance = Security()
