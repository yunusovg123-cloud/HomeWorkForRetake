import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(stored_hash: str, password: str) -> bool:
    return hash_password(password) == stored_hash
