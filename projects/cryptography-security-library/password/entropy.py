import math
import re
from collections import Counter
from typing import Dict


class PasswordEntropy:
    CHARSETS = {
        "lowercase": 26,
        "uppercase": 26,
        "digits": 10,
        "symbols": 33,
        "extended": 128,
    }

    COMMON_PATTERNS = {
        r"^(19|20)\d{2}$": "year",
        r"^\d{3,}$": "numbers",
        r"^[a-z]+$": "lowercase_only",
        r"^[A-Z]+$": "uppercase_only",
    }

    def calculate(self, password: str) -> float:
        charset_size = self._estimate_charset_size(password)
        length = len(password)

        if length == 0:
            return 0.0

        entropy = length * math.log2(charset_size)

        penalty = self._pattern_penalty(password)
        entropy -= penalty

        return max(entropy, 0.0)

    def _estimate_charset_size(self, password: str) -> int:
        size = 0
        if re.search(r"[a-z]", password):
            size += self.CHARSETS["lowercase"]
        if re.search(r"[A-Z]", password):
            size += self.CHARSETS["uppercase"]
        if re.search(r"\d", password):
            size += self.CHARSETS["digits"]
        if re.search(r"[^a-zA-Z0-9]", password):
            size += self.CHARSETS["symbols"]

        return size if size > 0 else self.CHARSETS["lowercase"]

    def _pattern_penalty(self, password: str) -> float:
        penalty = 0.0

        for pattern, name in self.COMMON_PATTERNS.items():
            if re.search(pattern, password):
                penalty += 10

        if len(set(password)) < len(password) * 0.5:
            penalty += 15

        if self._is_keyboard_pattern(password):
            penalty += 20

        if self._is_repeating(password):
            penalty += 15

        return penalty

    @staticmethod
    def _is_keyboard_pattern(password: str) -> bool:
        rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        lowered = password.lower()

        for row in rows:
            for i in range(len(row) - 2):
                pattern = row[i:i + 3]
                if pattern in lowered or pattern[::-1] in lowered:
                    return True
        return False

    @staticmethod
    def _is_repeating(password: str) -> bool:
        for i in range(len(password) - 2):
            if password[i] == password[i + 1] == password[i + 2]:
                return True
        return False

    @staticmethod
    def estimate_crack_time(entropy: float, guesses_per_second: float = 1e9) -> Dict[str, float]:
        combinations = 2 ** entropy
        seconds = combinations / guesses_per_second

        return {
            "seconds": seconds,
            "minutes": seconds / 60,
            "hours": seconds / 3600,
            "days": seconds / 86400,
            "years": seconds / 31536000,
        }
