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
        print(f"\n✓ Logged in as {user.name} (Teacher)")
        while True:
            print('\n--- Teacher Menu ---')
            print('1) Add homework')
            print('2) List homeworks')
            print('3) View submissions by homework ID')
            print('4) Grade submission')
            print('5) Logout')
            c = safe_input('Choose: ').strip()
            
            if c == '1':
                print('\nAvailable subjects:')
                for s in self.hw_service.SUBJECTS:
                    print(f'  - {s}')
                subject = safe_input('Subject: ').strip()
                if not subject:
                    print('Subject cannot be empty.')
                    continue
                desc = safe_input('Description: ').strip()
                if not desc:
                    print('Description cannot be empty.')
                    continue
                deadline = safe_input('Deadline (YYYY-MM-DD): ').strip()
                if not deadline:
                    print('Deadline cannot be empty.')
                    continue
                ftype = safe_input("Allowed file type ('pdf','docx','xlsx','any'): ").strip() or 'any'
                try:
                    hw = self.hw_service.create(subject, desc, deadline, ftype)
                    print(f'✓ Homework created. ID: {hw.id}')
                except Exception as e:
                    print(f'✗ Failed to create homework: {e}')
                safe_input('Press Enter to continue...')
            elif c == '2':
                hws = self.hw_service.list_all()
                if not hws:
                    print('No homeworks available.')
                else:
                    rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                    print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
                safe_input('Press Enter to continue...')
            elif c == '3':
                hid = safe_input('Enter homework ID: ').strip()
                if not hid.isdigit():
                    print('✗ Invalid ID. Must be a number.')
                    continue
                subs = self.sub_service.list_for_homework(int(hid))
                if not subs:
                    print(f'No submissions for homework ID {hid}.')
                else:
                    rows = []
                    for s in subs:
                        rows.append([s['id'], s['student_name'], s['uploaded_file'], s['submission_date'], 
                                   s.get('grade') or '-', s.get('teacher_comment') or '-'])
                    print_table(['ID', 'Student', 'File', 'Date', 'Grade', 'Comment'], rows)
                safe_input('Press Enter to continue...')
            elif c == '4':
                sid = safe_input('Enter submission ID to grade: ').strip()
                if not sid.isdigit():
                    print('✗ Invalid ID. Must be a number.')
                    continue
                grade = safe_input('Grade (e.g., A, 90): ').strip()
                if not grade:
                    print('Grade cannot be empty.')
                    continue
                comment = safe_input('Comment (or leave blank): ').strip()
                try:
                    self.sub_service.grade_submission(int(sid), grade, comment or None)
                    print(f'✓ Submission graded with grade: {grade}')
                except Exception as e:
                    print(f'✗ Failed to grade submission: {e}')
                safe_input('Press Enter to continue...')
            elif c == '5':
                print('Logged out.')
                break
            else:
                print('✗ Invalid choice. Please enter 1-5.')
