from typing import List, Optional
from database.db import Database
from models.homework import Homework


class HomeworkRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, subject_name: str, task_description: str, deadline: str, file_type: str) -> Homework:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO homeworks (subject_name, task_description, deadline, file_type) VALUES (?, ?, ?, ?)', (subject_name, task_description, deadline, file_type))
        conn.commit()
        hid = cur.lastrowid
        conn.close()
        return Homework(id=hid, subject_name=subject_name, task_description=task_description, deadline=deadline, file_type=file_type)

    def list_all(self) -> List[Homework]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT * FROM homeworks')
        rows = cur.fetchall()
        conn.close()
        return [Homework.from_row(r) for r in rows]

    def get_by_id(self, hw_id: int) -> Optional[Homework]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT * FROM homeworks WHERE id = ?', (hw_id,))
        row = cur.fetchone()
        conn.close()
        return Homework.from_row(row) if row else None

    def search(self, keyword: str) -> List[Homework]:
        conn = self.db.get_connection()
        like = f"%{keyword}%"
        cur = conn.execute('SELECT * FROM homeworks WHERE task_description LIKE ? OR subject_name LIKE ?', (like, like))
        rows = cur.fetchall()
        conn.close()
        return [Homework.from_row(r) for r in rows]

    def filter_by_subject(self, subject: str) -> List[Homework]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT * FROM homeworks WHERE subject_name = ?', (subject,))
        rows = cur.fetchall()
        conn.close()
        return [Homework.from_row(r) for r in rows]
