# Cryptography & Security Library

A comprehensive Python library demonstrating **modern cryptographic implementations**, **secure communication protocols**, **key management systems**, and **cryptographic attack simulations**. Built for learning, reference, and integration into security-critical applications.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Modules](#modules)
  - [Symmetric Encryption](#1-symmetric-encryption)
  - [Asymmetric Encryption](#2-asymmetric-encryption)
  - [Digital Signatures](#3-digital-signatures)
  - [Hash Functions](#4-hash-functions)
  - [Key Management](#5-key-management)
  - [Secure Communication](#6-secure-communication)
  - [Cryptographic Attacks](#7-cryptographic-attacks)
  - [Password Security](#8-password-security)
- [Usage Examples](#usage-examples)
- [Attack Demonstrations](#attack-demonstrations)
- [Best Practices](#best-practices)
- [References](#references)

## Overview

This library provides production-ready implementations of:

- **Symmetric encryption**: AES-GCM, ChaCha20-Poly1305, AES-CBC with HMAC
- **Asymmetric encryption**: RSA-OAEP, ECIES, hybrid encryption
- **Digital signatures**: RSA-PSS, ECDSA, Ed25519
- **Hash functions**: SHA-2/3, BLAKE2, PBKDF2, Argon2, bcrypt
- **Key management**: Generation, storage, rotation, splitting (Shamir's Secret Sharing)
- **Secure communication**: TLS-like handshake simulation, end-to-end encryption
- **Attack simulations**: Padding oracle, timing attacks, hash length extension, meet-in-the-middle
- **Password security**: Secure hashing, entropy calculation, breach checking

## Features

- **Modern algorithms only**: No deprecated algorithms (no DES, RC4, MD5 for security)
- **Authenticated encryption**: All encryption includes integrity verification
- **Forward secrecy**: Ephemeral key exchange support
- **Post-quantum ready**: Hybrid KEM implementations (Kyber + ECDH)
- **Constant-time operations**: Side-channel resistant implementations
- **Comprehensive testing**: Unit tests, known-answer tests, property-based tests
- **Well-documented**: Every function includes mathematical background and security considerations

## Project Structure

```
cryptography-security-library/
├── symmetric/
│   ├── __init__.py
│   ├── aes_gcm.py           # AES-256-GCM implementation
│   ├── chacha20.py          # ChaCha20-Poly1305 implementation
│   ├── aes_cbc.py           # AES-256-CBC with HMAC-SHA256
│   └── xchacha20.py         # XChaCha20-Poly1305 (extended nonce)
├── asymmetric/
│   ├── __init__.py
│   ├── rsa_oaep.py          # RSA-OAEP encryption/decryption
│   ├── ecies.py             # Elliptic Curve Integrated Encryption Scheme
│   ├── hybrid.py            # Hybrid encryption (KEM + DEM)
│   └── kyber_kem.py         # CRYSTALS-Kyber KEM (post-quantum)
├── signatures/
│   ├── __init__.py
│   ├── rsa_pss.py           # RSA-PSS signatures
│   ├── ecdsa.py             # ECDSA (P-256, P-384, P-521)
│   └── ed25519.py           # Ed25519 signatures
├── hashing/
│   ├── __init__.py
│   ├── sha_utils.py         # SHA-224/256/384/512
│   ├── sha3_utils.py        # SHA3-224/256/384/512, SHAKE128/256
│   ├── blake2.py            # BLAKE2b, BLAKE2s
│   └── key_derivation.py    # PBKDF2, Argon2id, bcrypt, scrypt
├── key_management/
│   ├── __init__.py
│   ├── key_generator.py     # Secure key generation
│   ├── key_store.py         # Encrypted key storage
│   ├── key_rotation.py      # Automatic key rotation policies
│   ├── shamir_secret.py     # Shamir's Secret Sharing
│   └── hsm_simulator.py     # Simulated HSM interface
├── protocols/
│   ├── __init__.py
│   ├── e2ee.py              # End-to-end encryption protocol
│   ├── secure_channel.py    # Secure communication channel
│   └── tls_handshake.py     # Simplified TLS 1.3 handshake
├── attacks/
│   ├── __init__.py
│   ├── padding_oracle.py    # Padding oracle attack demo
│   ├── timing_attack.py     # Timing attack demonstration
│   ├── hash_length_ext.py   # Hash length extension attack
│   └── mitm.py              # Meet-in-the-middle attack (2DES)
├── password/
│   ├── __init__.py
│   ├── hasher.py            # Secure password hashing
│   ├── entropy.py           # Password entropy calculation
│   └── strength.py          # Password strength meter
├── tests/
│   ├── test_symmetric.py
│   ├── test_asymmetric.py
│   ├── test_signatures.py
│   ├── test_hashing.py
│   ├── test_key_management.py
│   └── test_attacks.py
├── examples/
│   ├── encrypted_chat.py    # Simple encrypted chat example
│   ├── file_encryptor.py    # File encryption/decryption tool
│   └── secure_api.py        # API request signing example
├── requirements.txt
├── setup.py
├── Makefile
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Krtucho/cryptography-security-library.git
cd cryptography-security-library

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v
```

### Dependencies

```
cryptography>=41.0.0
pycryptodome>=3.20.0
pyshacl>=0.25.0  # For post-quantum schemes
nacl>=1.4.0      # libsodium bindings (Ed25519, XChaCha20)
```

## Modules

### 1. Symmetric Encryption

```python
from symmetric.aes_gcm import AESGCMEncryptor
from symmetric.chacha20 import ChaCha20Poly1305

# AES-256-GCM (authenticated encryption)
aes = AESGCMEncryptor()
key = aes.generate_key()  # 256-bit key
nonce = aes.generate_nonce()  # 96-bit nonce

ciphertext, tag = aes.encrypt(b"Hello, World!", key, nonce, aad=b"public_header")
plaintext = aes.decrypt(ciphertext, key, nonce, tag, aad=b"public_header")
assert plaintext == b"Hello, World!"

# ChaCha20-Poly1305 (AEAD)
chacha = ChaCha20Poly1305()
key = chacha.generate_key()
ciphertext = chacha.encrypt(b"Sensitive data", key, nonce=b"unique_nonce")
plaintext = chacha.decrypt(ciphertext, key, nonce=b"unique_nonce")
```

### 2. Asymmetric Encryption

```python
from asymmetric.rsa_oaep import RSAOAEPEncryptor
from asymmetric.ecies import ECIESEncryptor
from asymmetric.hybrid import HybridEncryptor

# RSA-OAEP (optimal asymmetric encryption padding)
rsa = RSAOAEPEncryptor()
private_key, public_key = rsa.generate_keypair(2048)

ciphertext = rsa.encrypt(b"Secret message", public_key)
plaintext = rsa.decrypt(ciphertext, private_key)

# ECIES (Elliptic Curve Integrated Encryption Scheme)
ecies = ECIESEncryptor(curve="secp256r1")
private_key, public_key = ecies.generate_keypair()

ciphertext = ecies.encrypt(b"Secret message", public_key)
plaintext = ecies.decrypt(ciphertext, private_key)

# Hybrid Encryption (KEM + DEM)
hybrid = HybridEncryptor()
ciphertext = hybrid.encrypt(b"Large message", recipient_public_key)
plaintext = hybrid.decrypt(ciphertext, recipient_private_key)
```

### 3. Digital Signatures

```python
from signatures.ed25519 import Ed25519Signer
from signatures.ecdsa import ECDSASigner
from signatures.rsa_pss import RSAPSSSigner

# Ed25519 (fast, secure signatures)
ed = Ed25519Signer()
private_key, public_key = ed.generate_keypair()

signature = ed.sign(b"Important document", private_key)
is_valid = ed.verify(b"Important document", signature, public_key)

# ECDSA with different curves
ecdsa = ECDSASigner(curve="P-256")
signature = ecdsa.sign(b"Data", private_key)
assert ecdsa.verify(b"Data", signature, public_key)

# RSA-PSS (probabilistic signature scheme)
rsa_signer = RSAPSSSigner()
signature = rsa_signer.sign(b"Contract", private_key)
assert rsa_signer.verify(b"Contract", signature, public_key)
```

### 4. Hash Functions

```python
from hashing.sha_utils import SHAUtils
from hashing.blake2 import BLAKE2Hasher
from hashing.key_derivation import KeyDerivation

# SHA-256/512
sha = SHAUtils()
digest = sha.sha256(b"Data to hash")
digest = sha.sha512(b"Data to hash")

# BLAKE2 (faster than SHA-3, secure)
blake = BLAKE2Hasher()
digest = blake.blake2b(b"Data", digest_size=64)
digest = blake.blake2s(b"Data", digest_size=32)

# Key derivation (password-based)
kdf = KeyDerivation()
# Argon2id (memory-hard, side-channel resistant)
hash = kdf.argon2id("password", salt=b"salt1234")
assert kdf.verify_argon2id("password", hash)

# PBKDF2-HMAC-SHA256 (NIST recommended)
hash = kdf.pbkdf2("password", salt=b"salt", iterations=600000)
assert kdf.verify_pbkdf2("password", hash)

# bcrypt
hash = kdf.bcrypt("password")
assert kdf.verify_bcrypt("password", hash)
```

### 5. Key Management

```python
from key_management.key_generator import KeyGenerator
from key_management.key_store import EncryptedKeyStore
from key_management.shamir_secret import ShamirSecretSharing

# Generate various key types
kg = KeyGenerator()
aes_key = kg.generate_symmetric_key(256)  # 32 bytes
rsa_keypair = kg.generate_rsa_keypair(2048)
ec_keypair = kg.generate_ec_keypair(curve="secp256r1")

# Encrypted key store
store = EncryptedKeyStore(master_password="strong-master-password")
store.store_key("my-aes-key", aes_key)
retrieved_key = store.retrieve_key("my-aes-key")

# Shamir's Secret Sharing (split a secret into N parts, need K to reconstruct)
sss = ShamirSecretSharing()
# Split into 5 shares, need any 3 to reconstruct
shares = sss.split(b"AES-256-key-here-1234567890abcde", total_shares=5, threshold=3)
# Reconstruct from any 3 shares
reconstructed = sss.reconstruct(shares[:3])
assert reconstructed == b"AES-256-key-here-1234567890abcde"
```

### 6. Secure Communication

```python
from protocols.e2ee import EndToEndEncryption
from protocols.secure_channel import SecureChannel

# End-to-end encryption (like Signal protocol concepts)
alice = EndToEndEncryption()
bob = EndToEndEncryption()

# Key exchange
alice_identity_key, alice_signed_prekey = alice.generate_identity()
bob_identity_key, bob_signed_prekey = bob.generate_identity()

# Establish session
alice_session = alice.initiate_session(bob_identity_key, bob_signed_prekey)
bob_session = bob.receive_session(alice_identity_key, alice_signed_prekey)

# Send encrypted message
ciphertext = alice_session.encrypt("Hello Bob! This is a secret message.")
plaintext = bob_session.decrypt(ciphertext)
assert plaintext == "Hello Bob! This is a secret message."

# Secure channel (authenticated, encrypted, with integrity)
channel = SecureChannel()
channel.establish(local_privkey, remote_pubkey)
encrypted = channel.send(b"Sensitive data")
decrypted = channel.receive(encrypted)
```

### 7. Cryptographic Attacks

```python
from attacks.padding_oracle import PaddingOracleAttack
from attacks.timing_attack import TimingAttack
from attacks.hash_length_ext import HashLengthExtensionAttack

# Padding Oracle Attack (against CBC mode)
oracle = PaddingOracleAttack(target_server)
# WARNING: For educational purposes only!
recovered = oracle.recover_plaintext(ciphertext)

# Timing Attack on HMAC comparison
attack = TimingAttack()
# Demonstrate why constant-time comparison is needed
vulnerable_time = attack.measure_comparison("key_a", "key_b", constant_time=False)
secure_time = attack.measure_comparison("key_a", "key_b", constant_time=True)

# Hash Length Extension (against naive MAC constructions)
hle = HashLengthExtensionAttack()
# Original: H(secret || message) — VULNERABLE!
original_mac = sha256(secret + message)
# Attacker can compute: H(secret || message || padding || extension)
forged_mac = hle.extend(original_mac, message, extension, key_len=16)
# The forged MAC is valid without knowing the secret!
```

### 8. Password Security

```python
from password.entropy import PasswordEntropy
from password.strength import PasswordStrengthMeter

# Calculate password entropy
entropy = PasswordEntropy()
print(entropy.calculate("correcthorsebatterystaple"))  # ~60 bits
print(entropy.calculate("P@ssw0rd"))  # ~30 bits (weak)

# Strength meter
meter = PasswordStrengthMeter()
result = meter.analyze("MySecureP@ssw0rd!2024")
print(result.score)  # 0-100
print(result.strength)  # weak/fair/strong/very_strong
print(result.crack_time_seconds)  # Estimated time to crack
print(result.feedback)  # Suggestions for improvement
```

## Usage Examples

### File Encryption Tool

```bash
# Encrypt a file
python examples/file_encryptor.py encrypt secret.pdf --output secret.pdf.enc

# Decrypt a file
python examples/file_encryptor.py decrypt secret.pdf.enc --output secret.pdf

# Encrypt with a key file
python examples/file_encryptor.py encrypt secret.pdf --key-file mykey.key

# Generate a new encryption key
python examples/file_encryptor.py generate-key --output mykey.key
```

### Encrypted Chat (End-to-End)

```bash
# Alice starts a server
python examples/encrypted_chat.py --mode server --port 8888

# Bob connects to Alice
python examples/encrypted_chat.py --mode client --host 127.0.0.1 --port 8888

# Messages are encrypted end-to-end with X3DH + AES-256-GCM
```

### API Request Signing

```python
from examples.secure_api import SecureAPIClient

client = SecureAPIClient(api_key="your-key", private_key=signing_key)

# Automatically signs every request
response = client.get("https://api.example.com/users")
response = client.post("https://api.example.com/data", json={"key": "value"})

# Headers added:
#   Authorization: Signature keyid="...",algorithm="ed25519",...
#   X-Timestamp: 2024-01-01T00:00:00Z
#   X-Nonce: unique-request-id
```

## Attack Demonstrations

### Padding Oracle Attack

```python
# This demonstrates why CBC mode + padding is dangerous
# and why authenticated encryption (GCM, ChaCha20-Poly1305) is preferred

oracle = PaddingOracleAttack(
    oracle_function=lambda ct: server.decrypt_and_validate_padding(ct)
)

# Recover plaintext without knowing the key
recovered = oracle.recover_block(encrypted_block)
print(f"Recovered plaintext block: {recovered}")
```

### Timing Attack on HMAC

```python
attack = TimingAttack()

# Standard comparison (vulnerable to timing attack)
times_vulnerable = []
for _ in range(1000):
    t = attack.measure_comparison("secret_key_123", "secret_key_456", constant_time=False)
    times_vulnerable.append(t)

# Constant-time comparison (secure)
times_secure = []
for _ in range(1000):
    t = attack.measure_comparison("secret_key_123", "secret_key_456", constant_time=True)
    times_secure.append(t)

print(f"Vulnerable stddev: {np.std(times_vulnerable):.6f}s")
print(f"Secure stddev: {np.std(times_secure):.6f}s")
# The vulnerable version has higher variance, leaking byte-by-byte comparison
```

## Best Practices

### Algorithm Selection

| Use Case | Recommended Algorithm | Key Size |
|----------|----------------------|----------|
| Symmetric encryption | AES-256-GCM | 256 bits |
| Symmetric encryption (high perf) | ChaCha20-Poly1305 | 256 bits |
| Asymmetric encryption | ECIES (X25519) | 256 bits |
| Asymmetric encryption (legacy) | RSA-OAEP | 4096 bits |
| Digital signatures | Ed25519 | 256 bits |
| Digital signatures (legacy) | RSA-PSS | 4096 bits |
| Key exchange | X25519 | 256 bits |
| Key exchange (post-quantum) | Kyber-768 + X25519 | hybrid |
| Password hashing | Argon2id | - |
| Password hashing (legacy) | bcrypt (cost=12) | - |
| Key derivation | HKDF-SHA256 | - |

### Cryptographic Pitfalls to Avoid

1. **Using ECB mode** — Leaks patterns in plaintext
2. **CBC mode without HMAC** — Vulnerable to padding oracle attacks
3. **Static nonces/IVs** — Destroys security of AES-GCM, ChaCha20
4. **MD5/SHA1 for signatures** — Collision attacks feasible
5. **RSA with PKCS#1 v1.5** — Vulnerable to Bleichenbacher attack
6. **Homemade cryptography** — Always use well-audited libraries
7. **Not authenticating ciphertext** — Leads to chosen-ciphertext attacks
8. **Using `==` for HMAC comparison** — Timing attack vulnerability

## References

- [NIST SP 800-175B](https://csrc.nist.gov/publications/detail/sp/800-175b/final) — Cryptographic Standards
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [IETF RFC 8446](https://tools.ietf.org/html/rfc8446) — TLS 1.3
- [IETF RFC 8439](https://tools.ietf.org/html/rfc8439) — ChaCha20-Poly1305
- [IETF RFC 8032](https://tools.ietf.org/html/rfc8032) — Ed25519
- [Argon2 RFC 9106](https://tools.ietf.org/html/rfc9106)
- [CRYSTALS-Kyber](https://pq-crystals.org/kyber/) — Post-quantum KEM
- [Libsodium Documentation](https://doc.libsodium.org/)

## License

MIT
