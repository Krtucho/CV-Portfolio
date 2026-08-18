import secrets
from typing import List, Tuple


class ShamirSecretSharing:
    """Shamir's Secret Sharing Scheme using GF(256)."""

    def __init__(self, prime: int = 2 ** 127 - 1):
        self.prime = prime

    def _random_polynomial(self, degree: int, secret: int) -> List[int]:
        coeffs = [secret]
        for _ in range(degree):
            coeffs.append(secrets.randbelow(self.prime))
        return coeffs

    def _evaluate_polynomial(self, coeffs: List[int], x: int) -> int:
        result = 0
        for coeff in reversed(coeffs):
            result = (result * x + coeff) % self.prime
        return result

    @staticmethod
    def _bytes_to_int(data: bytes) -> int:
        return int.from_bytes(data, byteorder="big")

    @staticmethod
    def _int_to_bytes(value: int, length: int) -> bytes:
        return value.to_bytes(length, byteorder="big")

    def split(self, secret: bytes, total_shares: int, threshold: int) -> List[Tuple[int, bytes]]:
        if threshold > total_shares:
            raise ValueError("Threshold cannot be larger than total shares")
        if threshold < 2:
            raise ValueError("Threshold must be at least 2")

        secret_int = self._bytes_to_int(secret)
        coeffs = self._random_polynomial(threshold - 1, secret_int)

        shares = []
        for i in range(1, total_shares + 1):
            value = self._evaluate_polynomial(coeffs, i)
            shares.append((i, self._int_to_bytes(value, len(secret))))

        return shares

    def reconstruct(self, shares: List[Tuple[int, bytes]]) -> bytes:
        if len(shares) < 2:
            raise ValueError("Need at least 2 shares for reconstruction")

        x_coords = [s[0] for s in shares]
        y_values = [self._bytes_to_int(s[1]) for s in shares]

        secret = 0
        for i in range(len(shares)):
            numerator = 1
            denominator = 1
            for j in range(len(shares)):
                if i != j:
                    numerator = (numerator * (-x_coords[j])) % self.prime
                    denominator = (denominator * (x_coords[i] - x_coords[j])) % self.prime

            lagrange = (y_values[i] * numerator * pow(denominator, -1, self.prime)) % self.prime
            secret = (secret + lagrange) % self.prime

        return self._int_to_bytes(secret, len(shares[0][1]))
