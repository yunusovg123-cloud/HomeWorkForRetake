from services.auth_service import AuthService
from services.homework_service import HomeworkService
from services.submission_service import SubmissionService
from utils.helpers import safe_input, print_table


class TeacherController:
    def __init__(self, auth: AuthService, hw_service: HomeworkService, sub_service: SubmissionService) -> None:
        self.auth = auth
        self.hw_service = hw_service
        self.sub_service = sub_service

    def menu(self, user) -> None:
        print(f"\nLogged in as {user.name} (teacher)")
        while True:
            print('\n-- Teacher Menu --')
            print('1) Add homework')
            print('2) List homeworks')
            print('3) View submissions by homework id')
            print('4) Grade submission')
            print('5) Logout')
            c = safe_input('Choose: ').strip()
            if c == '1':
                print('Subjects:')
                for s in self.hw_service.SUBJECTS:
                    print('-', s)
                subject = safe_input('Subject: ').strip()
                desc = safe_input('Description: ').strip()
                deadline = safe_input('Deadline (YYYY-MM-DD): ').strip()
                ftype = safe_input("Allowed file type ('pdf','docx','xlsx','any'): ").strip() or 'any'
                try:
                    hw = self.hw_service.create(subject, desc, deadline, ftype)
                    print('Created homework id', hw.id)
                except Exception as e:
                    print('Error:', e)
            elif c == '2':
                hws = self.hw_service.list_all()
                rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
            elif c == '3':
                hid = safe_input('Enter homework id: ').strip()
                if not hid.isdigit():
                    print('Invalid id')
                    continue
                subs = self.sub_service.list_for_homework(int(hid))
                rows = []
                for s in subs:
                    rows.append([s['id'], s['student_name'], s['uploaded_file'], s['submission_date'], s.get('grade') or '-', s.get('teacher_comment') or '-'])
                print_table(['ID', 'Student', 'File', 'Date', 'Grade', 'Comment'], rows)
            elif c == '4':
                sid = safe_input('Enter submission id to grade: ').strip()
                if not sid.isdigit():
                    print('Invalid id')
                    continue
                grade = safe_input('Grade (e.g., A, 90): ').strip()
                comment = safe_input('Comment: ').strip()
                try:
                    self.sub_service.grade_submission(int(sid), grade, comment)
                    print('Graded')
                except Exception as e:
                    print('Error:', e)
            elif c == '5':
                print('Logout')
                break
            else:
                print('Invalid choice')
