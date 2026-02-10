from typing import List, Optional
from database.db import Database
from models.user import User


class UserRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, name: str, phone: str, password_hash: str, role: str, group_number: Optional[str]) -> User:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (name, phone, password_hash, role, group_number) VALUES (?, ?, ?, ?, ?)', (name, phone, password_hash, role, group_number))
        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return User(id=uid, name=name, phone=phone, password_hash=password_hash, role=role, group_number=group_number)

    def list_all(self) -> List[User]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT * FROM users')
        rows = cur.fetchall()
        conn.close()
        return [User.from_row(r) for r in rows]

    def get_by_id(self, user_id: int) -> Optional[User]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cur.fetchone()
        conn.close()
        return User.from_row(row) if row else None

    def get_by_phone(self, phone: str) -> Optional[User]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT * FROM users WHERE phone = ?', (phone,))
        row = cur.fetchone()
        conn.close()
        return User.from_row(row) if row else None

    def update_password_hash(self, user_id: int, new_hash: str) -> None:
        conn = self.db.get_connection()
        conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))
        conn.commit()
        conn.close()
