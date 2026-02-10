from typing import Optional
from services.auth_service import AuthService
from utils.helpers import safe_input
from models.user import User


class AuthCLI:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth = auth_service
        self.MAX_PASSWORD_ATTEMPTS = 3

    def login_prompt(self) -> Optional[User]:
        """
        Prompt user for phone and password with improved error handling.
        
        Flow:
        1. Ask for phone number
        2. If exists, ask for password (hidden)
        3. If password wrong, allow up to 3 attempts, then return to phone entry
        4. If phone not found, offer to retry or exit
        """
        print('\n=== LOGIN ===')
        
        while True:
            # Phone entry loop
            phone = safe_input('Phone number (or type "exit" to quit): ').strip()
            if phone.lower() == 'exit':
                print('Cancelled.')
                return None
            
            if not phone:
                print('Phone number cannot be empty.')
                continue
            
            # Check if user exists
            user = self.auth.user_repo.get_by_phone(phone)
            if user is None:
                print('✗ User not found.')
                retry = safe_input('Try another phone number? (y/n): ').strip().lower()
                if retry != 'y':
                    return None
                continue
            
            # User found, prompt for password (up to 3 attempts)
            print(f'✓ User found: {user.name}')
            auth_user = self._password_attempt_loop(phone)
            if auth_user:
                print('✓ Login successful.')
                return auth_user
            else:
                # Password failed 3 times, return to phone entry
                print('Returning to phone number entry...')
                continue

    def _password_attempt_loop(self, phone: str) -> Optional[User]:
        """
        Handle password input with up to 3 attempts.
        
        Returns authenticated user or None if all attempts failed.
        """
        for attempt in range(1, self.MAX_PASSWORD_ATTEMPTS + 1):
            pwd = safe_input('Password: ')
            if pwd is None:
                return None
            
            auth_user = self.auth.authenticate(phone, pwd)
            if auth_user:
                return auth_user
            
            attempts_left = self.MAX_PASSWORD_ATTEMPTS - attempt
            if attempts_left > 0:
                print(f'✗ Incorrect password. Try again. ({attempts_left} attempts left)')
            else:
                print(f'✗ Incorrect password. Maximum attempts ({self.MAX_PASSWORD_ATTEMPTS}) reached.')
        
        return None
