# Competitive Programming Library Generator

Online judges accept a single source file. The tools here take a solution file
that uses code from this library and produce one self-contained file by pasting
the library code it uses in place of its `#include`s / imports.

- [Common](#common) - layout, `generate_new.py`, runner scripts, rules shared by both languages
- [C++](#c) - `cpcpp.sh` and the rules for `#include`s
- [Python](#python) - `cppy.sh` and the rules for imports

---

## Common

### Layout

| Path | Purpose |
|---|---|
| `<algorithm>/` (`union_find/`, `quicksort/`, `segtree/`, ...) | Library code, one folder per algorithm, `.cpp` and/or `.py` |
| `generate_new.py` | Amalgamates one solution file and prints the result to stdout |
| `amalgamater.py` | `CPPAmalgamater` and `PythonAmalgamater`, used by `generate_new.py` |
| `scripts/` | Runner scripts that amalgamate and run in one step |
| `ac-library/`, `generate_atcoder.py`, `atcoder/` | AtCoder Library submodule and its generated self-contained headers (see [C++](#atcoder-library)) |
| `generate.py` | Older whole-library generator (see below) |

### `generate_new.py`

```sh
python generate_new.py --main <solution file>
```

The language is chosen from the file extension (`.cpp` or `.py`). The
amalgamated source goes to stdout; nothing is compiled or run.

### Putting `scripts/` on PATH

**From bash (MinGW / Git Bash)** - source `add_scripts_to_path.sh`:

```sh
# current shell only
source ./add_scripts_to_path.sh

# current shell + append the export to ~/.bashrc (~/.zshrc under zsh)
source ./add_scripts_to_path.sh --permanent
```

**From PowerShell** - `add_scripts_to_path.ps1` does the same for Windows.
Because MSYS2 inherits and translates the Windows `PATH`, an entry added here
also shows up in later MinGW shells as `/c/Users/...`:

```powershell
# current session only (note the leading dot - it must be dot-sourced)
. .\add_scripts_to_path.ps1

# current session + permanently for the current user
. .\add_scripts_to_path.ps1 -Permanent

# permanently only, leaving the current session untouched
.\add_scripts_to_path.ps1 -Permanent
```

### Runner scripts

`scripts/cpcpp.sh` (C++) and `scripts/cppy.sh` (Python) share the same shape:

```sh
cpcpp.sh [-E|--emit] <solution.cpp> [extra g++ args...]
cppy.sh  [-E|--emit] <solution.py>  [program args...]
```

- `-E` / `--emit` prints the amalgamated source instead of running it - this is
  what you submit.
- The solution path may be relative or absolute; it is made absolute before
  being handed to `generate_new.py`, so the result does not depend on your
  current directory.
- The interpreter running `generate_new.py` is the first one that actually
  starts among every `python3` / `python` on `PATH`, then `py -3`. A plain
  lookup is not enough because a broken shim can shadow a working interpreter.
  Override it with `CPCPP_PYTHON` / `CPPY_PYTHON`.
- Temporary files come from `mktemp` and are removed on exit. Both are bash
  scripts, so run them from a MinGW / Git Bash shell, not `cmd`.

### Rules for the file to be amalgamated (both languages)

1. **Only reference library code through the language's include / import
   mechanism** described in the language section. Anything else is copied
   verbatim, so a library file referenced any other way is not pasted.
2. **Standard library includes / imports are left untouched** (`#include
   <vector>`, `from collections import deque`).
3. **Everything ends up in one file, so top-level names must not clash** across
   the solution and the library files it pulls in. In C++ a clash is a
   redefinition error; in Python the later definition silently wins.
4. **Pasted library files are copied as-is**, comments and all. Keep library
   files free of anything that should not be submitted (debug output, local
   file I/O).

### Whole-library generator (`generate.py`)

The older generator concatenates entire algorithm folders instead of following
a solution's includes / imports:

```sh
$ python generate.py  -h
usage: generate.py [-h] --lang {python,cpp} [--algos ALGOS [ALGOS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --lang {python,cpp}
  --algos ALGOS [ALGOS ...]
                        List of directories to include; all if unspecified
```

---

## C++

`CPPAmalgamater` replaces every `#include "..."` line with the (recursively
amalgamated) contents of that file. Roughly, `cpcpp.sh` does:

```sh
python3 generate_new.py --main <file> | g++ -std=c++17 -x c++ -o <tmp> - && <tmp>
```

### Prerequisite: use the UCRT64 shell (Windows)

Launch `C:\msys64\ucrt64.exe` (or `mingw64.exe`). **Not** the plain MSYS shell -
that environment has neither `g++` nor `python3` on `PATH`, so the script fails
with `command not found`.

Install the toolchain if needed:

```sh
pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-python
```

Verify:

```sh
$ which g++ python3
/ucrt64/bin/g++
/ucrt64/bin/python3
```

### Running it

```sh
$ cd ~/competitive_programming/codeforces/itmo-pilot-course
$ cpcpp.sh ./segment_tree_part_1_c_fix.cpp
$ cpcpp.sh ./segment_tree_part_1_c_fix.cpp -O2 -DLOCAL   # extra args go to g++
$ cpcpp.sh -E ./segment_tree_part_1_c_fix.cpp > submit.cpp
```

| Variable | Default | Meaning |
|---|---|---|
| `CXX` | `g++` | Compiler |
| `CPCPP_STD` | `-std=c++17` | Language standard flag |
| `CPCPP_PYTHON` | auto-detected | Interpreter for `generate_new.py` |

### AtCoder Library

`ac-library/` is a git submodule whose headers include each other through the
`ac-library/` include path. `generate_atcoder.py` expands each public header
into a self-contained file in `atcoder/` (plus an `atcoder/all` header), so a
solution can include them by relative path like any other library file:

```sh
git submodule update --init
python generate_atcoder.py   # re-run after every submodule update
```

### Rules for the file to be amalgamated

1. **Write library includes exactly as `#include "relative/path"`**: at the very
   start of the line, one space, double quotes, nothing after the closing
   quote (no trailing comment or whitespace). Two spaces or a trailing comment
   fail with `cannot resolve include`; an indented `#include` is copied
   verbatim and not pasted.
2. **Paths are relative to the file containing the `#include`**, e.g. from
   `~/competitive_programming/codeforces/round_1/a.cpp`:

   ```cpp
   #include "../../../competitive_programming_library/union_find/dsu.cpp"
   #include "../../../competitive_programming_library/atcoder/segtree.hpp"
   ```

   There is no include search path, so a path that does not exist relative to
   the including file is an error.
3. **`#include <...>` is never pasted** - system headers stay as they are. The
   line must end with `>`: `#include <vector> // comment` is mistaken for a
   library include and fails.

### Rules for library files

1. **The same rules apply recursively**: `#include "..."` lines inside a pasted
   library file are pasted too, relative to that library file.
2. **There is no "include once"**: a file reached twice is pasted twice. Library
   bodies here are not wrapped in include guards, so make sure each library
   file is reached only once (directly or through other library files), or wrap
   its body in `#ifndef` / `#define` / `#endif`. `#pragma once` does not help -
   after amalgamation everything is one file. (The generated `atcoder/` headers
   keep ac-library's own guards, so including those twice is fine.)
3. **Follow the existing convention for standard headers**, wrapping each in a
   guard named after it:

   ```cpp
   #ifndef __STD_VECTOR__
   #define __STD_VECTOR__
   #include <vector>
   #endif
   ```

---

## Python

`PythonAmalgamater` replaces each `from <package>.<module> import <names>` that
refers to a file in this library with that file's contents (pasted once, after
the modules it imports itself), then deletes the import. The library root is
the directory containing `amalgamater.py`.

### Setup: put the library root on the interpreter's path

So that solutions also run unamalgamated with a plain interpreter, add a `.pth`
file containing the library root to the site-packages of the interpreter you
use, e.g. the virtualenv at `~/competitive_programming/.venv`:

```sh
echo "C:/Users/admin/competitive_programming_library" > ~/competitive_programming/.venv/Lib/site-packages/cplib.pth
```

or, for whichever interpreter `python` currently is:

```sh
echo "C:/Users/admin/competitive_programming_library" > "$(python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')/cplib.pth"
```

A `.pth` file works for every way of starting that interpreter (terminal, IDE
run button, debugger). It is per interpreter - each Python install or venv
needs its own. Verify:

```sh
$ python -c "import union_find.dsu as m; print(m.__file__)"
C:\Users\admin\competitive_programming_library\union_find\dsu.py
```

### Running it

```sh
$ source ~/competitive_programming/.venv/Scripts/activate
$ cd ~/competitive_programming/misc
$ cppy.sh test_cplib.py < input.txt
$ cppy.sh test_cplib.py foo bar        # extra args go to the program (sys.argv)
$ cppy.sh -E test_cplib.py > submit.py
```

- With a virtualenv active, `cppy.sh` prefers `$VIRTUAL_ENV/Scripts/python.exe`
  (or `bin/python`) - a Windows venv only ships `python.exe`, so otherwise a
  system `python3` would win. `CPPY_PYTHON` overrides it.
- The amalgamated program is run with the same interpreter, from a temporary
  file, so it reads your stdin normally.
- The output is self-contained: it does not need the `.pth` file or this
  repository to run.

### Rules for the file to be amalgamated

1. **Import library code as `from <folder>.<module> import <names>`**, starting
   from the library root:

   ```python
   from union_find.dsu import DIS
   from quicksort.qs import q_sort as qs   # aliases become `qs = q_sort`
   ```

2. **No other import forms for library code.** `import union_find.dsu`,
   `from union_find import dsu` and `from union_find.dsu import *` are left in
   place and fail on a judge.
3. **Imports must be at the top level of the file** - not inside functions,
   `if` or `try` blocks, which are left untouched.
4. **No `sys.path` changes are needed.** If present (e.g. a
   `__file__`-relative append of the library root for an interpreter without
   the `.pth`), every top-level `sys.path.*(...)` call is deleted.
5. **No relative imports** in the solution itself - it is run as a script, not
   as part of a package, so they are an error.

### Rules for library modules

1. **Import siblings with relative imports** (`from .dsu import
   DSU_Iterative_By_Size`) or the same absolute form as solutions
   (`from union_find.dsu import ...`). Both are resolved the way the
   interpreter resolves them.
2. **Relative imports must name a module**: `from .module import name`, not
   `from . import module`. An unresolvable relative import, or one going above
   the top-level package (`from ...x import y` in `union_find/dsu.py`), is an
   error.
3. **No `sys.path` changes** in library modules.
4. **Folder names must be importable and must not shadow standard modules**:
   valid identifiers (no hyphens) and not `random`, `queue`, `heapq`, etc.
   `__init__.py` files are optional.
5. **Module-level code should only define things.** Each module is pasted
   once, in place of its first import, after the modules it imports. Import
   cycles work as long as they work under the plain interpreter.
6. **Self-tests go under `if __name__ == "__main__":`** - such blocks are
   dropped from pasted library modules (but kept in the solution).
7. **`from __future__` imports are allowed**; they are moved to the top of the
   output.
8. **Files are read as UTF-8.**
