from services.auth_service import AuthService
from services.homework_service import HomeworkService
from services.submission_service import SubmissionService
from cli.student_cli import StudentController
from cli.teacher_cli import TeacherController
from cli.auth_cli import AuthCLI
from utils.helpers import safe_input, select_numeric_menu


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
                self._create_user_menu()
            elif choice == '3':
                print('Bye!')
                break
            else:
                print('Invalid choice. Please enter 1-3.')

    def _create_user_menu(self) -> None:
        """Handle user registration with improved UX for role selection."""
        print('\n=== Create User ===')
        name = safe_input('Name: ').strip()
        if not name:
            print('Name cannot be empty.')
            return
        
        # Role selection using numeric menu
        role_choice = select_numeric_menu(['Student', 'Teacher'], 'Select role: ')
        if role_choice == -1:
            return
        role = 'student' if role_choice == 1 else 'teacher'
        
        phone = safe_input('Phone number: ').strip()
        if not phone:
            print('Phone number cannot be empty.')
            return
        
        pwd = safe_input('Set password: ')
        if not pwd:
            print('Password cannot be empty.')
            return
        
        group = None
        if role == 'student':
            group = safe_input('Group number: ').strip() or None
        
        try:
            self.auth.register_user(name, phone, pwd, role, group)
            print('✓ User created successfully.')
        except Exception as e:
            print(f'✗ Error creating user: {e}')
