from typing import Optional
from services.auth_service import AuthService
from utils.helpers import safe_input
from models.user import User


try:
    # getpass may not work in some IDE consoles; import here and fallback if needed
    from getpass import getpass
except Exception:
    def getpass(prompt: str = '') -> str:  # type: ignore
        return input(prompt)


class AuthCLI:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth = auth_service

    def login_prompt(self) -> Optional[User]:
        print('\n=== LOGIN ===')
        while True:
            phone = safe_input('Enter phone number (or type exit): ').strip()
            if phone.lower() == 'exit':
                return None
            if not phone:
                print('Empty input. Please enter phone number or type exit to quit.')
                continue
            user = self.auth.user_repo.get_by_phone(phone)
            if user is None:
                print('User not found')
                choice = safe_input("Retry login? (y/n): ").strip().lower()
                if choice != 'y':
                    return None
                continue
            # prompt password using visible input, up to 3 attempts
            attempts = 0
            while attempts < 3:
                pwd = safe_input('Enter password: ')
                if pwd is None:
                    print('\nInput cancelled')
                    return None
                auth_user = self.auth.authenticate(phone, pwd)
                if auth_user:
                    print('Login successful')
                    return auth_user
                else:
                    attempts += 1
                    print(f'Incorrect password ({attempts}/3)')
            print('Too many failed attempts. Exiting.')
            return None
