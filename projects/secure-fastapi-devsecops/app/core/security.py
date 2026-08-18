import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

from app.core.config import settings


class UnauthorizedError(Exception):
    pass


class RateLimitExceeded(Exception):
    pass


class PasswordHasher:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


class TokenManager:
    @staticmethod
    def create_access_token(subject: str, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": subject,
            "role": role,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access",
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh",
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid token")


class EncryptionService:
    def __init__(self):
        self._fernet = Fernet(secrets.token_bytes(32))

    def encrypt(self, data: str) -> str:
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        return self._fernet.decrypt(encrypted_data.encode()).decode()


class CryptoService:
    @staticmethod
    def generate_rsa_keypair() -> tuple[bytes, bytes]:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return private_pem, public_pem

    @staticmethod
    def sign_data(private_key_pem: bytes, data: bytes) -> bytes:
        private_key = load_pem_private_key(private_key_pem, password=None)
        signature = private_key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return signature

    @staticmethod
    def verify_signature(public_key_pem: bytes, data: bytes, signature: bytes) -> bool:
        public_key = load_pem_public_key(public_key_pem)
        try:
            public_key.verify(signature, data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
            return True
        except Exception:
            return False

    @staticmethod
    def hash_data(data: str, algorithm: str = "sha256") -> str:
        h = hashlib.new(algorithm)
        h.update(data.encode())
        return h.hexdigest()

    @staticmethod
    def hmac_sign(key: bytes, message: bytes) -> str:
        return hmac.new(key, message, hashlib.sha256).hexdigest()
