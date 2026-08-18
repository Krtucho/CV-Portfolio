from cryptography.hazmat.primitives.asymmetric import ed25519


class Ed25519Signer:
    def generate_keypair(self) -> tuple:
        private_key = ed25519.Ed25519PrivateKey.generate()
        return private_key, private_key.public_key()

    def sign(self, data: bytes, private_key) -> bytes:
        return private_key.sign(data)

    def verify(self, data: bytes, signature: bytes, public_key) -> bool:
        try:
            public_key.verify(signature, data)
            return True
        except Exception:
            return False

    @staticmethod
    def sign_message(private_key_pem: bytes, message: bytes) -> bytes:
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        private_key = load_pem_private_key(private_key_pem, password=None)
        return private_key.sign(message)
