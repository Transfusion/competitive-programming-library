
import os
import re
from pathlib import Path


def resolve_path(path, *paths) -> str:
    return Path(os.path.join(path, *paths)).resolve()

class CPPAmalgamater(object):
    def __init__(self, include_paths: list[str] = None):
        self._include_paths = [str(Path(p).resolve()) for p in (include_paths or [])]

    def _is_not_stl(self, include_path: str):
        return not include_path.startswith('<') and not include_path.endswith('>')
        # return "competitive-programming-library" in include_path and not include_path.startswith('<') and not include_path.endswith('>')

    def _is_include(self, line: str):
        return line.startswith("#include")

    def get_include_path(self, line: str) -> str | None:
        if not self._is_include(line) or not self._is_not_stl(line):
            return None
        return line.replace("#include", "")[2:-1]

    def _resolve_include(self, base_dir: str, include_path: str) -> str:
        local = resolve_path(base_dir, include_path)
        if os.path.isfile(local):
            return local
        for search_dir in self._include_paths:
            candidate = resolve_path(search_dir, include_path)
            if os.path.isfile(candidate):
                return candidate
        raise FileNotFoundError(f"cannot resolve include: {include_path} from {base_dir}")

    def _amalgamate(self, abs_path: str):
        base_dir = os.path.dirname(abs_path)
        contents = open(os.path.join(abs_path)).read()
        split_lines = contents.splitlines()

        res = []

        for line in split_lines:
            include_path = self.get_include_path(line)
            if include_path is not None:
                res.extend(self._amalgamate(self._resolve_include(base_dir, include_path)))
            else:
                res.append(line)
        return res

    def amalgamate(self, abs_path: str):
        return "\n".join(self._amalgamate(abs_path))

class PythonAmalgamater(object):
    def __init__(self):
        self._sys_paths = []

    def _is_relative_import(self, line: str):
        return line.startswith("from .")

    def _is_import(self, line: str):
        return line.startswith("from ") or line.startswith("import ")

    def _get_relative_include_path(self, line: str) -> str | None:
        if not self._is_import(line) or not self._is_relative_import(line):
            return None
        module_path = line.split()[1]
        leading_dots = len(module_path) - len(module_path.lstrip('.'))
        relative_part = module_path[leading_dots:]
        if not relative_part:
            return None
        parts = relative_part.split('.')
        if leading_dots > 1:
            parts = ['..'] * (leading_dots - 1) + parts
        return os.path.join(*parts) + '.py'

    def _parse_sys_path_line(self, line: str, base_dir: str) -> str | None:
        """Extract the resolved directory from a sys.path.append/insert call."""
        stripped = line.strip()
        if 'sys.path.append(' not in stripped and 'sys.path.insert(' not in stripped:
            return None
        string_literals = re.findall(r"['\"]([^'\"]*)['\"]", stripped)
        if not string_literals:
            return None
        if '__file__' in stripped:
            return str(resolve_path(base_dir, *string_literals))
        return str(resolve_path(os.getcwd(), *string_literals))

    def _resolve_sys_path_import(self, line: str) -> str | None:
        """Try to resolve a bare import against accumulated sys.path entries."""
        if not self._is_import(line) or self._is_relative_import(line):
            return None
        parts = line.split()
        module_name = parts[1].rstrip(',') if parts[0] == "import" else parts[1]
        if '.' in module_name:
            return None
        for sys_path_dir in self._sys_paths:
            candidate = os.path.join(sys_path_dir, module_name + '.py')
            if os.path.isfile(candidate):
                return candidate
        return None

    def _amalgamate(self, abs_path: str):
        base_dir = os.path.dirname(abs_path)
        contents = open(os.path.join(abs_path)).read()
        split_lines = contents.splitlines()

        res = []

        for line in split_lines:
            sys_path_dir = self._parse_sys_path_line(line, base_dir)
            if sys_path_dir is not None:
                self._sys_paths.append(sys_path_dir)
                continue

            rel_path = self._get_relative_include_path(line)
            if rel_path is not None:
                res.extend(self._amalgamate(resolve_path(base_dir, rel_path)))
                continue

            sys_path_file = self._resolve_sys_path_import(line)
            if sys_path_file is not None:
                res.extend(self._amalgamate(sys_path_file))
                continue

            res.append(line)
        return res

    def amalgamate(self, abs_path: str):
        self._sys_paths = []
        return "\n".join(self._amalgamate(abs_path))
