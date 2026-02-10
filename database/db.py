import os
import sqlite3
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'homework_cli.db')


class Database:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or DB_PATH

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        # If DB exists but has old schema (no phone/password_hash), recreate it to apply new schema
        if os.path.exists(self.db_path):
            conn_check = self.get_connection()
            cur = conn_check.cursor()
            try:
                cur.execute("PRAGMA table_info(users)")
                cols = [r['name'] for r in cur.fetchall()]
                if 'phone' in cols and 'password_hash' in cols:
                    conn_check.close()
                    return
            except Exception:
                # if any error, fall through to recreate DB
                pass
            conn_check.close()
            try:
                os.remove(self.db_path)
            except Exception:
                pass
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            group_number TEXT
        )
        ''')
        cur.execute('''
        CREATE TABLE homeworks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            task_description TEXT NOT NULL,
            deadline TEXT NOT NULL,
            file_type TEXT NOT NULL
        )
        ''')
        cur.execute('''
        CREATE TABLE submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            homework_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            uploaded_file TEXT NOT NULL,
            submission_date TEXT NOT NULL,
            grade TEXT,
            teacher_comment TEXT,
            FOREIGN KEY(homework_id) REFERENCES homeworks(id),
            FOREIGN KEY(student_id) REFERENCES users(id)
        )
        ''')
        # Seed users with phone and hashed passwords
        try:
            from utils.security import hash_password
        except Exception:
            # fallback simple sha256
            import hashlib
            def hash_password(p):
                return hashlib.sha256(p.encode('utf-8')).hexdigest()

        cur.execute("INSERT INTO users (name, phone, password_hash, role, group_number) VALUES (?, ?, ?, ?, ?)", ('Teacher Ali', '998901112233', hash_password('teacher123'), 'teacher', None))
        cur.execute("INSERT INTO users (name, phone, password_hash, role, group_number) VALUES (?, ?, ?, ?, ?)", ('Student Malika', '998931234567', hash_password('student123'), 'student', '101'))
        cur.execute("INSERT INTO users (name, phone, password_hash, role, group_number) VALUES (?, ?, ?, ?, ?)", ('Student Yusuf', '998939999999', hash_password('student456'), 'student', '101'))
        # Seed homeworks
        homeworks = [
            ('Matematika', 'Solve problems 1-10 from chapter 3', '2026-03-10', 'pdf'),
            ('Dasturlash', 'Implement sorting algorithm in any language', '2026-03-05', 'any'),
            ('WebSite', 'Create a simple HTML page', '2026-03-12', 'any'),
            ('Ingliz tili', 'Read passage and write summary', '2026-03-08', 'docx')
        ]
        cur.executemany('INSERT INTO homeworks (subject_name, task_description, deadline, file_type) VALUES (?, ?, ?, ?)', homeworks)
        conn.commit()
        conn.close()
