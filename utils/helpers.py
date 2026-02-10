from typing import List, Any


def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print('\nInput cancelled')
        return ''


def select_numeric_menu(options: List[str], prompt: str = 'Choose: ') -> int:
    """
    Display numbered menu options and return user's 1-based choice.
    
    Args:
        options: List of option labels (e.g., ['Student', 'Teacher'])
        prompt: Prompt text
    
    Returns:
        1-based selected index, or -1 if invalid/cancelled
    """
    while True:
        for i, opt in enumerate(options, start=1):
            print(f'{i}) {opt}')
        choice = safe_input(prompt).strip()
        if not choice:
            print('Empty input. Please select a valid option.')
            continue
        if choice.lower() == 'exit':
            print('Cancelled.')
            return -1
        if not choice.isdigit():
            print('Invalid choice. Please enter a number.')
            continue
        choice_int = int(choice)
        if 1 <= choice_int <= len(options):
            return choice_int
        else:
            print(f'Invalid choice. Please enter 1-{len(options)}.')


def print_table(headers: List[str], rows: List[List[Any]]) -> None:
    # simple column widths
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    sep = ' | '
    line = '+'.join('-' * (w + 2) for w in widths)
    # header
    hdr = sep.join(h.ljust(widths[i]) for i, h in enumerate(headers))
    print(line)
    print(hdr)
    print(line)
    for r in rows:
        print(sep.join(str(r[i]).ljust(widths[i]) for i in range(len(headers))))
    print(line)
