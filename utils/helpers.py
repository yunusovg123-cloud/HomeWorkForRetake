from typing import List, Any


def safe_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print('\nInput cancelled')
        return ''


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
