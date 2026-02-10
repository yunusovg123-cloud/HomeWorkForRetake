from dataclasses import dataclass


@dataclass
class Homework:
    id: int
    subject_name: str
    task_description: str
    deadline: str
    file_type: str

    @classmethod
    def from_row(cls, row):
        return cls(id=row['id'], subject_name=row['subject_name'], task_description=row['task_description'], deadline=row['deadline'], file_type=row['file_type'])
