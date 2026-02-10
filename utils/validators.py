from typing import List
import os


EXT_GROUPS = {
    'pdf': ['pdf'],
    'docx': ['doc', 'docx'],
    'xlsx': ['xls', 'xlsx'],
    'any': ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg']
}


def is_valid_date(date_str: str) -> bool:
    # Expect YYYY-MM-DD
    try:
        parts = date_str.split('-')
        if len(parts) != 3:
            return False
        y, m, d = map(int, parts)
        return 1 <= m <= 12 and 1 <= d <= 31 and y >= 1900
    except Exception:
        return False


def get_extension(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip('.').lower()


def is_valid_submission_extension(filename: str, required_type: str) -> bool:
    ext = get_extension(filename)
    allowed = EXT_GROUPS.get(required_type, [])
    return ext in allowed
