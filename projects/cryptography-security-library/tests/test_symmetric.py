from symmetric.aes_gcm import AESGCMEncryptor


def test_aes_gcm_encrypt_decrypt():
    encryptor = AESGCMEncryptor()
    key = encryptor.generate_key()
    nonce = encryptor.generate_nonce()
    plaintext = b"Hello, World! This is a test message."

    ciphertext, used_nonce = encryptor.encrypt(plaintext, key, nonce)
    decrypted = encryptor.decrypt(ciphertext, key, used_nonce)

    assert decrypted == plaintext
    assert len(key) == 32
    assert len(nonce) == 12


def test_aes_gcm_with_aad():
    encryptor = AESGCMEncryptor()
    key = encryptor.generate_key()
    nonce = encryptor.generate_nonce()
    plaintext = b"Sensitive data"
    aad = b"public_header_info"

    ciphertext, used_nonce = encryptor.encrypt(plaintext, key, nonce, aad)
    decrypted = encryptor.decrypt(ciphertext, key, used_nonce, aad=aad)

    assert decrypted == plaintext


def test_aes_gcm_tampered_ciphertext():
    encryptor = AESGCMEncryptor()
    key = encryptor.generate_key()
    plaintext = b"Test data"

    ciphertext, nonce = encryptor.encrypt(plaintext, key)
    tampered = bytearray(ciphertext)
    tampered[0] ^= 0xFF

    try:
        encryptor.decrypt(bytes(tampered), key, nonce)
        assert False, "Should have raised an exception for tampered ciphertext"
    except Exception:
        pass


def test_aes_gcm_wrong_key():
    encryptor = AESGCMEncryptor()
    key1 = encryptor.generate_key()
    key2 = encryptor.generate_key()
    plaintext = b"Test data"

    ciphertext, nonce = encryptor.encrypt(plaintext, key1)

    try:
        encryptor.decrypt(ciphertext, key2, nonce)
        assert False, "Should have raised an exception for wrong key"
    except Exception:
        pass
