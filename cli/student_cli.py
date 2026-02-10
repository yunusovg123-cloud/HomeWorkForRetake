from services.auth_service import AuthService
from services.homework_service import HomeworkService
from services.submission_service import SubmissionService
from utils.helpers import safe_input, print_table


class StudentController:
    def __init__(self, auth: AuthService, hw_service: HomeworkService, sub_service: SubmissionService) -> None:
        self.auth = auth
        self.hw_service = hw_service
        self.sub_service = sub_service

    def menu(self, user) -> None:
        print(f"\n✓ Logged in as {user.name} (Student)")
        while True:
            print('\n--- Student Menu ---')
            print('1) List homeworks')
            print('2) Search homeworks')
            print('3) Filter by subject')
            print('4) Homework details')
            print('5) Submit homework')
            print('6) View my submission history')
            print('7) Logout')
            c = safe_input('Choose: ').strip()
            
            if c == '1':
                hws = self.hw_service.list_all()
                if not hws:
                    print('No homeworks available.')
                else:
                    rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                    print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
                safe_input('Press Enter to continue...')
            elif c == '2':
                q = safe_input('Enter keyword: ').strip()
                if not q:
                    print('Search keyword cannot be empty.')
                    continue
                hws = self.hw_service.search(q)
                if not hws:
                    print(f'No homeworks found matching "{q}".')
                else:
                    rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                    print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
                safe_input('Press Enter to continue...')
            elif c == '3':
                print('\nAvailable subjects:')
                for s in self.hw_service.SUBJECTS:
                    print(f'  - {s}')
                subj = safe_input('Select subject: ').strip()
                if not subj:
                    print('Subject cannot be empty.')
                    continue
                hws = self.hw_service.filter_by_subject(subj)
                if not hws:
                    print(f'No homeworks found for subject "{subj}".')
                else:
                    rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                    print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
                safe_input('Press Enter to continue...')
            elif c == '4':
                hid = safe_input('Enter homework ID: ').strip()
                if not hid.isdigit():
                    print('✗ Invalid ID. Must be a number.')
                    continue
                hw = self.hw_service.get(int(hid))
                if hw is None:
                    print('✗ Homework not found.')
                else:
                    print('\n--- Homework Details ---')
                    print(f'ID: {hw.id}')
                    print(f'Subject: {hw.subject_name}')
                    print(f'Description: {hw.task_description}')
                    print(f'Deadline: {hw.deadline}')
                    print(f'Allowed file type: {hw.file_type}')
                safe_input('Press Enter to continue...')
            elif c == '5':
                hid = safe_input('Enter homework ID to submit: ').strip()
                if not hid.isdigit():
                    print('✗ Invalid ID. Must be a number.')
                    continue
                filename = safe_input('Enter filename/path (simulated): ').strip()
                if not filename:
                    print('Filename cannot be empty.')
                    continue
                try:
                    res = self.sub_service.submit(int(hid), user.id, filename)
                    print(f'✓ Submission successful: {res}')
                except Exception as e:
                    print(f'✗ Submission failed: {e}')
                safe_input('Press Enter to continue...')
            elif c == '6':
                subs = self.sub_service.list_for_student(user.id)
                if not subs:
                    print('No submissions yet.')
                else:
                    rows = []
                    for s in subs:
                        rows.append([s['id'], s['homework_id'], s['subject_name'], s['uploaded_file'], 
                                   s['submission_date'], s.get('grade') or '-', s.get('teacher_comment') or '-'])
                    print_table(['ID', 'HW_ID', 'Subject', 'File', 'Date', 'Grade', 'Comment'], rows)
                safe_input('Press Enter to continue...')
            elif c == '7':
                print('Logged out.')
                break
            else:
                print('✗ Invalid choice. Please enter 1-7.')
