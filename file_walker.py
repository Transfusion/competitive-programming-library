from dataclasses import dataclass

from parser import Parser

import os, collections

from pathlib import Path

@dataclass
class ImportToReplace:
    """Imports to replace and their actual file contents"""
    entire_line: str
    path: str
    resolved_path: str

def walk(file_path: str, parser: Parser) -> list[ImportToReplace]:

    def resolve_path(path, *paths) -> str:
        return Path(os.path.join(path, *paths)).resolve()

    def get_includes(file_path: str) -> str:
        contents = open(os.path.join(file_path)).read()
        return parser.parse_includes(contents)

    resolved_path = resolve_path(file_path)
    base_dir = os.path.dirname(resolved_path)
    print("resolving path", resolved_path, base_dir)

    res = []

    q = collections.deque(get_includes(resolved_path))

    while q:
        n = len(q)
        for _ in range(n):
            item = q.popleft()
            print("???", item)
            resolved_item = resolve_path(base_dir, item.path)
            res.append( ImportToReplace(item.entire_line, item.path, resolved_item) )
            q.extend(get_includes(resolved_item))

    # print("done", res)
    # print(q)
    return res
