
import ast
import importlib.util
import os
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
    """Inlines library modules imported with `from <package>.<module> import <names>`.

    Modules resolve against the library root (this file's directory, which is also
    on the interpreter's sys.path via a .pth file); relative imports inside the
    library are resolved the way the interpreter does. Each module is inlined once,
    after the modules it imports, in place of its first import; resolved imports are
    deleted and `as` aliases become assignments. Other imports (stdlib, third party)
    are kept.
    """

    def __init__(self):
        self._root = Path(__file__).resolve().parent
        self._visited = set()
        self._future = []

    def amalgamate(self, abs_path: str) -> str:
        path = Path(abs_path).resolve()
        self._visited = {path}
        self._future = []
        body = self._amalgamate(path, package=None)
        return "\n".join(self._future + body)

    def _amalgamate(self, path: Path, package: str | None) -> list[str]:
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        replacements = {}
        for node in ast.parse(source, filename=str(path)).body:
            new_lines = self._rewrite(node, source, package)
            if new_lines is not None:
                replacements[node.lineno - 1] = (node.end_lineno, new_lines)

        res = []
        i = 0
        while i < len(lines):
            if i in replacements:
                i, new_lines = replacements[i]
                res.extend(new_lines)
            else:
                res.append(lines[i])
                i += 1
        return res

    def _rewrite(self, node: ast.stmt, source: str, package: str | None) -> list[str] | None:
        """Return the lines replacing a top-level statement, or None to keep it."""
        if isinstance(node, ast.ImportFrom):
            return self._hoist_future(node, source) if node.module == "__future__" else self._inline_import(node, package)
        if self._is_sys_path_statement(node) or (package is not None and self._is_main_guard(node)):
            return []
        return None

    def _inline_import(self, node: ast.ImportFrom, package: str | None) -> list[str] | None:
        spec = "." * node.level + (node.module or "")
        found = self._module_file(importlib.util.resolve_name(spec, package))
        if found is None:
            if node.level:
                raise ImportError(f"cannot resolve relative import {spec!r} in package {package!r} (use `from .module import name`)")
            return None
        path, module_package = found
        res = []
        if path not in self._visited:
            self._visited.add(path)
            res = self._amalgamate(path, module_package)
        res.extend(f"{a.asname} = {a.name}" for a in node.names if a.asname and a.asname != a.name)
        return res

    def _module_file(self, name: str) -> tuple[Path, str] | None:
        """The file under the library root defining module `name`, and that module's package."""
        base = self._root.joinpath(*name.split("."))
        if base.with_name(base.name + ".py").is_file():
            return base.with_name(base.name + ".py").resolve(), name.rpartition(".")[0]
        if (base / "__init__.py").is_file():
            return (base / "__init__.py").resolve(), name
        return None

    # Extras: cases the library does not rely on today, handled so they cannot break the output.

    def _hoist_future(self, node: ast.ImportFrom, source: str) -> list[str]:
        """`from __future__` imports must open the file, so collect them for the top."""
        segment = ast.get_source_segment(source, node)
        if segment not in self._future:
            self._future.append(segment)
        return []

    @staticmethod
    def _is_sys_path_statement(node: ast.stmt) -> bool:
        """sys.path edits (e.g. a __file__-relative append of the library root) are obsolete once inlined."""
        return (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Call)
            and ast.unparse(node.value.func).startswith("sys.path.")
        )

    @staticmethod
    def _is_main_guard(node: ast.stmt) -> bool:
        """`if __name__ == "__main__":` in a library module would run its self-test."""
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            return False
        operands = [node.test.left, *node.test.comparators]
        return (
            len(operands) == 2
            and isinstance(node.test.ops[0], ast.Eq)
            and any(isinstance(o, ast.Name) and o.id == "__name__" for o in operands)
            and any(isinstance(o, ast.Constant) and o.value == "__main__" for o in operands)
        )

