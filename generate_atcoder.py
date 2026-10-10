"""Generates self-contained amalgamated headers from the ac-library submodule.

Each public header in ac-library/atcoder/*.hpp is expanded into a single
self-contained file in atcoder/ so external projects can use relative imports
without adding ac-library/ to the include path.

Usage: python generate_atcoder.py
Re-run after every `git submodule update`.
"""

import os

from amalgamater import CPPAmalgamater

AC_LIBRARY_DIR = os.path.join(os.path.dirname(__file__), "ac-library")
ATCODER_SRC_DIR = os.path.join(AC_LIBRARY_DIR, "atcoder")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "atcoder")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    amalgamater = CPPAmalgamater(include_paths=[AC_LIBRARY_DIR])

    for filename in sorted(os.listdir(ATCODER_SRC_DIR)):
        if not filename.endswith(".hpp") or filename.startswith("internal_"):
            continue

        src_path = os.path.join(ATCODER_SRC_DIR, filename)
        content = amalgamater.amalgamate(src_path)
        out_path = os.path.join(OUTPUT_DIR, filename)

        with open(out_path, "w") as f:
            f.write(content + "\n")

        print(f"generated: atcoder/{filename}")

    # Generate the `all` convenience header
    public_headers = [
        f for f in sorted(os.listdir(OUTPUT_DIR)) if f.endswith(".hpp")
    ]
    all_path = os.path.join(OUTPUT_DIR, "all")
    with open(all_path, "w") as f:
        for h in public_headers:
            f.write(f'#include "{h}"\n')
    print(f"generated: atcoder/all")


if __name__ == "__main__":
    main()
