from cli.menus import Menus
from database.db import Database
from services.auth_service import AuthService
from services.homework_service import HomeworkService
from services.submission_service import SubmissionService


class CLIApp:
    def __init__(self) -> None:
        self.db = Database()
        self.db.init_db()
        self.auth_service = AuthService(self.db)
        self.homework_service = HomeworkService(self.db)
        self.submission_service = SubmissionService(self.db)
        self.menus = Menus(self.auth_service, self.homework_service, self.submission_service)

    def run(self) -> None:
        self.menus.main_menu()
