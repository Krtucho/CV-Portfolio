import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AESGCMEncryptor:
    KEY_SIZE = 32
    NONCE_SIZE = 12

    def generate_key(self) -> bytes:
        return AESGCM.generate_key(bit_length=self.KEY_SIZE * 8)

    @staticmethod
    def generate_nonce() -> bytes:
        return os.urandom(12)

    def encrypt(self, plaintext: bytes, key: bytes, nonce: bytes = None, aad: bytes = None) -> tuple:
        if nonce is None:
            nonce = self.generate_nonce()
        if len(key) != self.KEY_SIZE:
            raise ValueError(f"Key must be {self.KEY_SIZE} bytes")
        if len(nonce) != self.NONCE_SIZE:
            raise ValueError(f"Nonce must be {self.NONCE_SIZE} bytes")

        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, aad or b"")
        return ciphertext, nonce

    def decrypt(self, ciphertext: bytes, key: bytes, nonce: bytes, tag: bytes = None, aad: bytes = None) -> bytes:
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, aad or b"")
