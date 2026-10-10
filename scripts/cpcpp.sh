#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
    echo "usage: cpcpp.sh [-E|--emit] <source.cpp> [extra g++ args...]" >&2
    echo "       -E, --emit   print the amalgamated source to stdout instead of building" >&2
}

EMIT=0
while [ $# -gt 0 ]; do
    case "$1" in
        -E|--emit) EMIT=1; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; break ;;
        *) break ;;
    esac
done

if [ $# -lt 1 ]; then
    usage
    exit 2
fi

SRC="$1"
shift
if [ ! -f "$SRC" ]; then
    echo "cpcpp: no such file: $SRC" >&2
    exit 1
fi
if [[ "$SRC" != /* ]]; then
    SRC="$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")"
fi

# Pick the first interpreter that actually runs. A plain `python3` lookup is not
# enough: a broken shim (e.g. a uv trampoline pointing at a removed install) can
# shadow a working interpreter later in PATH.
PY=()
if [ -n "${CPCPP_PYTHON:-}" ]; then
    PY=("$CPCPP_PYTHON")
else
    while IFS= read -r candidate; do
        if "$candidate" -c '' >/dev/null 2>&1; then
            PY=("$candidate")
            break
        fi
    done < <(type -aPf python3 python 2>/dev/null || true)
    if [ ${#PY[@]} -eq 0 ] && py -3 -c '' >/dev/null 2>&1; then
        PY=(py -3)
    fi
fi
if [ ${#PY[@]} -eq 0 ]; then
    echo "cpcpp: no working Python interpreter found (tried every python3/python on PATH, and py -3)" >&2
    echo "       set CPCPP_PYTHON=/path/to/python to choose one explicitly" >&2
    exit 1
fi

CXX="${CXX:-g++}"
CXXSTD="${CPCPP_STD:--std=c++17}"

OUT="$(mktemp -t cpcpp.XXXXXXXXXX)"
GEN="$(mktemp -t cpcpp.XXXXXXXXXX)"
trap 'rm -f "$OUT" "$GEN"' EXIT

if ! "${PY[@]}" "$LIB_DIR/generate_new.py" --main "$SRC" > "$GEN"; then
    echo "cpcpp: code generation failed (${PY[*]})" >&2
    exit 1
fi
if [ ! -s "$GEN" ]; then
    echo "cpcpp: code generation produced no output (${PY[*]})" >&2
    exit 1
fi

if [ "$EMIT" -eq 1 ]; then
    cat "$GEN"
    exit 0
fi

"$CXX" "$CXXSTD" -x c++ -o "$OUT" "$GEN" "$@"
"$OUT"
