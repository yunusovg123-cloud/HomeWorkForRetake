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
        print(f"\nLogged in as {user.name} (student)")
        while True:
            print('\n-- Student Menu --')
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
                rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
            elif c == '2':
                q = safe_input('Keyword: ').strip()
                hws = self.hw_service.search(q)
                rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
            elif c == '3':
                print('Subjects:')
                for s in self.hw_service.SUBJECTS:
                    print('-', s)
                subj = safe_input('Subject: ').strip()
                hws = self.hw_service.filter_by_subject(subj)
                rows = [[hw.id, hw.subject_name, hw.task_description, hw.deadline, hw.file_type] for hw in hws]
                print_table(['ID', 'Subject', 'Description', 'Deadline', 'FileType'], rows)
            elif c == '4':
                hid = safe_input('Enter homework id: ').strip()
                if not hid.isdigit():
                    print('Invalid id')
                    continue
                hw = self.hw_service.get(int(hid))
                if hw is None:
                    print('Not found')
                else:
                    print('\n--- Homework Detail ---')
                    print('ID:', hw.id)
                    print('Subject:', hw.subject_name)
                    print('Description:', hw.task_description)
                    print('Deadline:', hw.deadline)
                    print('Allowed file type:', hw.file_type)
            elif c == '5':
                hid = safe_input('Enter homework id to submit: ').strip()
                if not hid.isdigit():
                    print('Invalid id')
                    continue
                filename = safe_input('Enter filename/path to submit (simulated): ').strip()
                try:
                    res = self.sub_service.submit(int(hid), user.id, filename)
                    print('Submitted:', res)
                except Exception as e:
                    print('Error:', e)
            elif c == '6':
                subs = self.sub_service.list_for_student(user.id)
                rows = []
                for s in subs:
                    rows.append([s['id'], s['homework_id'], s['subject_name'], s['uploaded_file'], s['submission_date'], s.get('grade') or '-', s.get('teacher_comment') or '-'])
                print_table(['ID', 'HW_ID', 'Subject', 'File', 'Date', 'Grade', 'Comment'], rows)
            elif c == '7':
                print('Logout')
                break
            else:
                print('Invalid choice')
