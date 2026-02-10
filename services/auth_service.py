from repositories.user_repository import UserRepository
from database.db import Database
from models.user import User
from typing import Optional
from utils.security import hash_password, verify_password


class AuthService:
    def __init__(self, db: Database) -> None:
        self.user_repo = UserRepository(db)

    def list_users(self) -> list[User]:
        return self.user_repo.list_all()

    def register_user(self, name: str, phone: str, password: str, role: str, group_number: Optional[str]) -> User:
        pw_hash = hash_password(password)
        return self.user_repo.create(name, phone, pw_hash, role, group_number)

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def authenticate(self, phone: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_phone(phone)
        if not user:
            return None
        stored = user.password_hash or ''
        # detect if stored is likely a SHA256 hex (64 hex chars)
        is_hash = False
        if isinstance(stored, str) and len(stored) == 64:
            try:
                int(stored, 16)
                is_hash = True
            except ValueError:
                is_hash = False

        if is_hash:
            # regular hashed compare
            if verify_password(stored, password):
                return user
            return None
        else:
            # legacy/plaintext stored password: compare directly, then migrate to hashed
            if stored == password:
                new_h = hash_password(password)
                try:
                    self.user_repo.update_password_hash(user.id, new_h)
                    user.password_hash = new_h
                except Exception:
                    # non-fatal: proceed without stopping login
                    pass
                return user
            return None
