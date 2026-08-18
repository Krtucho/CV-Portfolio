import hashlib
import secrets

import bcrypt


class KeyDerivation:
    @staticmethod
    def pbkdf2(password: str, salt: bytes = None, iterations: int = 600000, dklen: int = 32) -> str:
        if salt is None:
            salt = secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=dklen)
        return f"$pbkdf2-sha256${iterations}${salt.hex()}${dk.hex()}"

    @staticmethod
    def verify_pbkdf2(password: str, stored_hash: str) -> bool:
        parts = stored_hash.split("$")
        iterations = int(parts[2])
        salt = bytes.fromhex(parts[3])
        dk_expected = bytes.fromhex(parts[4])
        dk_actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, dklen=len(dk_expected))
        return secrets.compare_digest(dk_actual, dk_expected)

    @staticmethod
    def bcrypt_hash(password: str, rounds: int = 12) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=rounds)).decode()

    @staticmethod
    def verify_bcrypt(password: str, stored_hash: str) -> bool:
        return bcrypt.checkpw(password.encode(), stored_hash.encode())

    @staticmethod
    def argon2id(password: str, salt: bytes = None) -> str:
        try:
            from argon2 import PasswordHasher
            ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16)
            return ph.hash(password)
        except ImportError:
            raise ImportError("Install argon2-cffi: pip install argon2-cffi")

    @staticmethod
    def verify_argon2id(password: str, stored_hash: str) -> bool:
        try:
            from argon2 import PasswordHasher
            ph = PasswordHasher()
            return ph.verify(stored_hash, password)
        except ImportError:
            raise ImportError("Install argon2-cffi: pip install argon2-cffi")
