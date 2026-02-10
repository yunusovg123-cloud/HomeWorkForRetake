from database.db import Database
from repositories.homework_repository import HomeworkRepository
from models.homework import Homework
from typing import List, Optional


class HomeworkService:
    SUBJECTS = ['Matematika', 'Dasturlash', 'WebSite', 'Ingliz tili']

    def __init__(self, db: Database) -> None:
        self.repo = HomeworkRepository(db)

    def list_all(self) -> List[Homework]:
        return self.repo.list_all()

    def create(self, subject_name: str, task_description: str, deadline: str, file_type: str) -> Homework:
        return self.repo.create(subject_name, task_description, deadline, file_type)

    def get(self, hw_id: int) -> Optional[Homework]:
        return self.repo.get_by_id(hw_id)

    def search(self, keyword: str) -> List[Homework]:
        return self.repo.search(keyword)

    def filter_by_subject(self, subject: str) -> List[Homework]:
        return self.repo.filter_by_subject(subject)
