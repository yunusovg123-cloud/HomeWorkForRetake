from typing import List, Optional
from database.db import Database
from models.submission import Submission


class SubmissionRepository:
    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, homework_id: int, student_id: int, uploaded_file: str, submission_date: str) -> Submission:
        conn = self.db.get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO submissions (homework_id, student_id, uploaded_file, submission_date) VALUES (?, ?, ?, ?)', (homework_id, student_id, uploaded_file, submission_date))
        conn.commit()
        sid = cur.lastrowid
        conn.close()
        return Submission(id=sid, homework_id=homework_id, student_id=student_id, uploaded_file=uploaded_file, submission_date=submission_date)

    def list_by_homework(self, homework_id: int) -> List[Submission]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT s.*, u.name as student_name FROM submissions s JOIN users u ON s.student_id = u.id WHERE homework_id = ?', (homework_id,))
        rows = cur.fetchall()
        conn.close()
        # Return rows as dicts (include student_name)
        return rows

    def list_by_student(self, student_id: int) -> List[Submission]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT s.*, h.subject_name FROM submissions s JOIN homeworks h ON s.homework_id = h.id WHERE s.student_id = ?', (student_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def get_by_id(self, sub_id: int) -> Optional[Submission]:
        conn = self.db.get_connection()
        cur = conn.execute('SELECT s.*, u.name as student_name, h.subject_name FROM submissions s JOIN users u ON s.student_id = u.id JOIN homeworks h ON s.homework_id = h.id WHERE s.id = ?', (sub_id,))
        row = cur.fetchone()
        conn.close()
        return row

    def grade(self, sub_id: int, grade: str, comment: str) -> None:
        conn = self.db.get_connection()
        conn.execute('UPDATE submissions SET grade = ?, teacher_comment = ? WHERE id = ?', (grade, comment, sub_id))
        conn.commit()
        conn.close()
