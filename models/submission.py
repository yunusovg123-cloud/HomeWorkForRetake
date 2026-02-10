from dataclasses import dataclass
from typing import Optional


@dataclass
class Submission:
    id: int
    homework_id: int
    student_id: int
    uploaded_file: str
    submission_date: str
    grade: Optional[str] = None
    teacher_comment: Optional[str] = None

    @classmethod
    def from_row(cls, row):
        return cls(id=row['id'], homework_id=row['homework_id'], student_id=row['student_id'], uploaded_file=row['uploaded_file'], submission_date=row['submission_date'], grade=row['grade'], teacher_comment=row['teacher_comment'])
