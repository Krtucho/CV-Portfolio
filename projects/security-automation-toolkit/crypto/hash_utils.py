import hashlib
import hmac
from pathlib import Path
from typing import Dict, List, Optional


class HashUtils:
    COMMON_PASSWORDS = [
        "123456", "password", "12345678", "qwerty", "123456789",
        "12345", "1234", "111111", "1234567", "sunshine",
        "qwerty123", "iloveyou", "princess", "admin", "welcome",
        "666666", "abc123", "football", "123123", "monkey",
    ]

    WEAK_HASHES = {"md5", "sha1", "sha224"}

    @staticmethod
    def hash_file(file_path: Path, algorithm: str = "sha256") -> str:
        h = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def verify_file_hash(file_path: Path, expected_hash: str, algorithm: str = "sha256") -> bool:
        actual_hash = HashUtils.hash_file(file_path, algorithm)
        return hmac.compare_digest(actual_hash, expected_hash)

    @staticmethod
    def hash_data(data: str, algorithm: str = "sha256") -> str:
        return hashlib.new(algorithm, data.encode()).hexdigest()

    @staticmethod
    def detect_hash_algorithm(hash_string: str) -> Optional[str]:
        length = len(hash_string)
        algo_map = {
            32: "MD5",
            40: "SHA1",
            56: "SHA224",
            64: "SHA256",
            96: "SHA384",
            128: "SHA512",
        }
        return algo_map.get(length)

    @staticmethod
    def is_weak_hash(hash_string: str) -> bool:
        algo = HashUtils.detect_hash_algorithm(hash_string)
        return algo.lower() in HashUtils.WEAK_HASHES if algo else False

    @staticmethod
    def crack_md5_hash(target_hash: str) -> Optional[str]:
        if len(target_hash) != 32:
            return None

        for password in HashUtils.COMMON_PASSWORDS:
            if hashlib.md5(password.encode()).hexdigest() == target_hash:
                return password
        return None

    @staticmethod
    def detect_weak_hashes(shadow_file: Path) -> List[Dict[str, str]]:
        weak = []
        try:
            for line in shadow_file.read_text().split("\n"):
                if ":" in line and "$" in line:
                    parts = line.split(":")
                    username = parts[0]
                    hash_part = parts[1]
                    algo_id = hash_part.split("$")[1] if hash_part.count("$") >= 2 else ""

                    algo_names = {"1": "MD5", "2a": "Blowfish", "5": "SHA256", "6": "SHA512"}
                    if algo_id == "1":
                        weak.append({
                            "username": username,
                            "hash_type": "MD5",
                            "hash": hash_part[:40],
                            "risk": "high",
                            "recommendation": "Upgrade to SHA512 ($6$)",
                        })
        except Exception:
            pass
        return weak

    @staticmethod
    def generate_salted_hash(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        import secrets
        salt = salt or secrets.token_hex(16).encode()
        h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)
        return {
            "hash": h.hex(),
            "salt": salt.decode() if isinstance(salt, bytes) else salt,
            "algorithm": "PBKDF2-HMAC-SHA256",
            "iterations": "100000",
        }

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str, salt: str) -> bool:
        h = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), salt.encode(), 100000)
        return hmac.compare_digest(h.hex(), stored_hash)
