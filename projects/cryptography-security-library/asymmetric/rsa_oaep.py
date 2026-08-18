from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class RSAOAEPEncryptor:
    def generate_keypair(self, key_size: int = 2048) -> tuple:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        return private_key, private_key.public_key()

    def encrypt(self, plaintext: bytes, public_key) -> bytes:
        return public_key.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    def decrypt(self, ciphertext: bytes, private_key) -> bytes:
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    @staticmethod
    def serialize_private_key(private_key, password: bytes = None) -> bytes:
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=(
                serialization.BestAvailableEncryption(password)
                if password else serialization.NoEncryption()
            ),
        )

    @staticmethod
    def serialize_public_key(public_key) -> bytes:
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
