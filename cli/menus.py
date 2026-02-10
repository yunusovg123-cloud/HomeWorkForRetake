from services.auth_service import AuthService
from services.homework_service import HomeworkService
from services.submission_service import SubmissionService
from cli.student_cli import StudentController
from cli.teacher_cli import TeacherController
from cli.auth_cli import AuthCLI
from utils.helpers import safe_input


class Menus:
    def __init__(self, auth: AuthService, hw_service: HomeworkService, sub_service: SubmissionService) -> None:
        self.auth = auth
        self.hw_service = hw_service
        self.sub_service = sub_service
        self.student_ctrl = StudentController(self.auth, self.hw_service, self.sub_service)
        self.teacher_ctrl = TeacherController(self.auth, self.hw_service, self.sub_service)
        self.auth_cli = AuthCLI(self.auth)

    def main_menu(self) -> None:
        while True:
            print('\n=== HomeWork CLI ===')
            print('1) Login as existing user')
            print('2) Create user')
            print('3) Exit')
            choice = safe_input('Choose: ').strip()
            if choice == '1':
                user = self.auth_cli.login_prompt()
                if user is None:
                    continue
                if user.role == 'student':
                    self.student_ctrl.menu(user)
                else:
                    self.teacher_ctrl.menu(user)
            elif choice == '2':
                name = safe_input('Name: ').strip()
                role = ''
                while role not in ('student', 'teacher'):
                    role = safe_input("Role ('student' or 'teacher'): ").strip()
                group = None
                phone = safe_input('Phone number: ').strip()
                from getpass import getpass
                pwd = getpass('Set password: ')
                if role == 'student':
                    group = safe_input('Group number: ').strip() or None
                try:
                    self.auth.register_user(name, phone, pwd, role, group)
                    print('User created')
                except Exception as e:
                    print('Error creating user:', e)
            elif choice == '3':
                print('Bye')
                break
            else:
                print('Invalid choice')
