#!/usr/bin/env python3
"""Phase Echo challenge primitives. Public code intentionally models a faulty telemetry path."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# SEC 2 / NIST P-256 domain parameters.
P = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
A = P - 3
B = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
GX = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
GY = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
N = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
G = (GX, GY)
UNKNOWN_BITS = 80
DOMAIN = b"RYNEX/PHASE-ECHO/V1\x00"
TELEMETRY_DOMAIN = b"PX/telemetry/calibration/v3/"


def point_add(left: tuple[int, int] | None,
              right: tuple[int, int] | None) -> tuple[int, int] | None:
    """Affine short-Weierstrass addition; None is the point at infinity."""
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if left == right:
        slope = ((3 * x1 * x1 + A) * pow(2 * y1, -1, P)) % P
    else:
        slope = ((y2 - y1) * pow((x2 - x1) % P, -1, P)) % P
    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return x3, y3


def point_mul(scalar: int, point: tuple[int, int] = G) -> tuple[int, int] | None:
    """Double-and-add scalar multiplication."""
    result = None
    addend = point
    while scalar:
        if scalar & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        scalar >>= 1
    return result


def message_digest(message: bytes) -> int:
    return int.from_bytes(hashlib.sha256(DOMAIN + message).digest(), "big") % N


def sign(private_key: int, message: bytes, nonce: int) -> tuple[int, int]:
    point = point_mul(nonce)
    if point is None:
        raise ValueError("invalid nonce")
    r = point[0] % N
    s = (pow(nonce, -1, N) * (message_digest(message) + r * private_key)) % N
    if r == 0 or s == 0:
        raise ValueError("degenerate signature")
    return r, s


def derive_aead_key(private_key: int, public_x: int, public_y: int) -> bytes:
    """Key schedule used by the fictional vault service."""
    ikm = private_key.to_bytes(32, "big") + public_x.to_bytes(32, "big") + public_y.to_bytes(32, "big")
    return hashlib.sha256(b"PhaseEcho vault key v1\x00" + ikm).digest()


def telemetry_label(nonce: int, message: bytes) -> int:
    """Return a calibrated diagnostic word from a signing event."""
    mask = int.from_bytes(hashlib.sha256(TELEMETRY_DOMAIN + message).digest()[:22], "big")
    return (nonce >> UNKNOWN_BITS) ^ mask


def build_artifact(flag: str, seed: bytes, count: int = 56) -> dict[str, Any]:
    """Author helper: make a bundle. Keep its seed and flag private."""
    if not flag.startswith("RTCTF{") or not flag.endswith("}"):
        raise ValueError("flag must use RTCTF{...} format")
    private_key = int.from_bytes(hashlib.sha256(b"signer\x00" + seed).digest(), "big") % (N - 1) + 1
    pub = point_mul(private_key)
    assert pub is not None
    records = []
    for index in range(count):
        message = (f"archive=PX-{index:03d}; shard={hashlib.sha256(seed + index.to_bytes(4, 'big')).hexdigest()[:24]}").encode()
        nonce_material = hashlib.shake_256(b"nonce\x00" + seed + index.to_bytes(4, "big")).digest(48)
        nonce = int.from_bytes(nonce_material, "big") % (N - 1) + 1
        r, s = sign(private_key, message, nonce)
        records.append({
            "message": message.decode("ascii"),
            "digest": f"{message_digest(message):064x}",
            "r": f"{r:064x}",
            "s": f"{s:064x}",
            # A calibration mask was mixed into this diagnostic field.
            "phase": f"{telemetry_label(nonce, message):056x}",
        })
    pub_hex = f"{pub[0]:064x}{pub[1]:064x}"
    key = derive_aead_key(private_key, pub[0], pub[1])
    nonce_aead = hashlib.sha256(b"vault nonce\x00" + seed).digest()[:12]
    aad = b"Rynex Phase Echo sealed archive v1"
    ciphertext = AESGCM(key).encrypt(nonce_aead, flag.encode("ascii"), aad)
    return {
        "format": "PHASE-ECHO/1",
        "curve": "P-256",
        "public_key_xy": pub_hex,
        "nonce_unknown_bits": UNKNOWN_BITS,
        "records": records,
        "vault": {
            "kdf": "SHA-256(\"PhaseEcho vault key v1\\0\" || d32 || Qx32 || Qy32)",
            "aead": "AES-256-GCM",
            "nonce": nonce_aead.hex(),
            "aad": aad.decode("ascii"),
            "ciphertext_and_tag": ciphertext.hex(),
        },
    }


def pretty_json(obj: dict[str, Any]) -> str:
    return json.dumps(obj, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    print("Phase Echo · Rynex Technologies · Cryptography")
    print(f"P-256 order: {N:064x}")
    print("Captured public instance: output.txt")
