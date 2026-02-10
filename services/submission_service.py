from database.db import Database
from repositories.submission_repository import SubmissionRepository
from repositories.homework_repository import HomeworkRepository
from datetime import datetime
from utils.validators import is_valid_submission_extension
from typing import List, Optional


class SubmissionService:
    def __init__(self, db: Database) -> None:
        self.repo = SubmissionRepository(db)
        self.hw_repo = HomeworkRepository(db)

    def submit(self, homework_id: int, student_id: int, filename: str) -> dict:
        hw = self.hw_repo.get_by_id(homework_id)
        if hw is None:
            raise ValueError('Homework not found')
        if not is_valid_submission_extension(filename, hw.file_type):
            raise ValueError('File type not allowed for this homework')
        now = datetime.now().isoformat()
        sub = self.repo.create(homework_id, student_id, filename, now)
        return {'id': sub.id, 'uploaded_file': sub.uploaded_file, 'date': sub.submission_date}

    def list_for_homework(self, homework_id: int) -> List[dict]:
        rows = self.repo.list_by_homework(homework_id)
        return [dict(r) for r in rows]

    def list_for_student(self, student_id: int) -> List[dict]:
        rows = self.repo.list_by_student(student_id)
        return [dict(r) for r in rows]

    def get_submission(self, sub_id: int) -> Optional[dict]:
        row = self.repo.get_by_id(sub_id)
        return dict(row) if row else None

    def grade_submission(self, sub_id: int, grade: str, comment: str) -> None:
        self.repo.grade(sub_id, grade, comment)
