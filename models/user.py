from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    phone: str
    password_hash: str
    role: str
    group_number: Optional[str]

    @classmethod
    def from_row(cls, row):
        return cls(id=row['id'], name=row['name'], phone=row['phone'], password_hash=row['password_hash'], role=row['role'], group_number=row['group_number'])
