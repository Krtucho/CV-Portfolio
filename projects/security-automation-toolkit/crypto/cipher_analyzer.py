from dataclasses import dataclass
from typing import List
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher


@dataclass
class CipherAnalysis:
    name: str
    key_size: int
    mode: str
    security_level: str
    is_deprecated: bool
    recommendations: List[str]


class CipherAnalyzer:
    CIPHER_DATABASE = {
        "AES-256-GCM": {
            "security_level": "strong",
            "deprecated": False,
            "recommendations": [],
            "key_size": 256,
            "mode": "GCM",
        },
        "AES-128-GCM": {
            "security_level": "strong",
            "deprecated": False,
            "recommendations": ["Consider AES-256-GCM for higher security"],
            "key_size": 128,
            "mode": "GCM",
        },
        "AES-256-CBC": {
            "security_level": "moderate",
            "deprecated": False,
            "recommendations": [
                "Prefer GCM mode over CBC (authenticated encryption)",
                "Ensure HMAC is used for integrity",
            ],
            "key_size": 256,
            "mode": "CBC",
        },
        "AES-128-CBC": {
            "security_level": "moderate",
            "deprecated": False,
            "recommendations": [
                "Consider AES-256-GCM for better security",
                "Use HMAC for integrity verification",
            ],
            "key_size": 128,
            "mode": "CBC",
        },
        "DES": {
            "security_level": "weak",
            "deprecated": True,
            "recommendations": [
                "DES is BROKEN and should not be used",
                "Migrate to AES-256-GCM immediately",
            ],
            "key_size": 56,
            "mode": "CBC",
        },
        "3DES": {
            "security_level": "weak",
            "deprecated": True,
            "recommendations": [
                "3DES is deprecated due to Sweet32 attack",
                "Migrate to AES-256-GCM immediately",
            ],
            "key_size": 168,
            "mode": "CBC",
        },
        "RC4": {
            "security_level": "broken",
            "deprecated": True,
            "recommendations": [
                "RC4 is COMPLETELY BROKEN",
                "Migrate to AES-256-GCM immediately",
                "Multiple attacks exist (Fluhrer, Mantin, Shamir)",
            ],
            "key_size": 128,
            "mode": "stream",
        },
        "Blowfish": {
            "security_level": "weak",
            "deprecated": True,
            "recommendations": [
                "Blowfish is deprecated (64-bit block size)",
                "Migrate to AES or ChaCha20",
            ],
            "key_size": 448,
            "mode": "CBC",
        },
        "ChaCha20-Poly1305": {
            "security_level": "strong",
            "deprecated": False,
            "recommendations": [],
            "key_size": 256,
            "mode": "AEAD",
        },
    }

    def analyze_cipher(self, cipher_name: str) -> CipherAnalysis:
        info = self.CIPHER_DATABASE.get(cipher_name)
        if not info:
            return CipherAnalysis(
                name=cipher_name,
                key_size=0,
                mode="unknown",
                security_level="unknown",
                is_deprecated=False,
                recommendations=["Unknown cipher - verify the implementation"],
            )
        return CipherAnalysis(
            name=cipher_name,
            key_size=info["key_size"],
            mode=info["mode"],
            security_level=info["security_level"],
            is_deprecated=info["deprecated"],
            recommendations=info["recommendations"],
        )

    def scan_cipher_suites(self, cipher_list: List[str]) -> List[CipherAnalysis]:
        return [self.analyze_cipher(c) for c in cipher_list]

    def get_strong_ciphers(self) -> List[str]:
        return [
            name for name, info in self.CIPHER_DATABASE.items()
            if info["security_level"] == "strong" and not info["deprecated"]
        ]

    def generate_report(self, analyses: List[CipherAnalysis]) -> str:
        lines = ["Cipher Analysis Report", "=" * 50]
        for a in analyses:
            status = "✅ SECURE" if a.security_level == "strong" else "⚠️ WEAK" if a.security_level in {"moderate", "weak"} else "❌ BROKEN"
            lines.extend([
                f"\nCipher: {a.name} ({a.key_size}-bit, {a.mode})",
                f"Status: {status}",
                f"Deprecated: {a.is_deprecated}",
            ])
            if a.recommendations:
                lines.append(f"Recommendations:")
                for r in a.recommendations:
                    lines.append(f"  - {r}")
        return "\n".join(lines)
