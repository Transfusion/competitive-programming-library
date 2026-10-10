#!/usr/bin/env bash
# Adds the scripts/ directory of this repository to PATH.
# Must be sourced to affect the current shell:
#     source ./add_scripts_to_path.sh [--permanent]

_cpl_permanent=0
for _cpl_arg in "$@"; do
    case "$_cpl_arg" in
        -p|--permanent) _cpl_permanent=1 ;;
        *) echo "usage: source add_scripts_to_path.sh [--permanent]" >&2; return 2 2>/dev/null || exit 2 ;;
    esac
done

if [ -n "${BASH_SOURCE[0]:-}" ]; then
    _cpl_self="${BASH_SOURCE[0]}"
    [ "${BASH_SOURCE[0]}" = "$0" ] && _cpl_sourced=0 || _cpl_sourced=1
elif [ -n "${ZSH_VERSION:-}" ]; then
    _cpl_self="${(%):-%x}"
    case "$ZSH_EVAL_CONTEXT" in *:file) _cpl_sourced=1 ;; *) _cpl_sourced=0 ;; esac
else
    _cpl_self="$0"
    _cpl_sourced=0
fi

_cpl_root="$(cd "$(dirname "$_cpl_self")" && pwd)"
_cpl_scripts_dir="$_cpl_root/scripts"

case ":$PATH:" in
    *":$_cpl_scripts_dir:"*) ;;
    *) PATH="$_cpl_scripts_dir:$PATH"; export PATH ;;
esac

if [ "$_cpl_permanent" -eq 1 ]; then
    if [ -n "${ZSH_VERSION:-}" ]; then
        _cpl_rc="$HOME/.zshrc"
    else
        _cpl_rc="$HOME/.bashrc"
    fi
    _cpl_line="export PATH=\"$_cpl_scripts_dir:\$PATH\""
    if [ -f "$_cpl_rc" ] && grep -Fqx "$_cpl_line" "$_cpl_rc"; then
        echo "Already in $_cpl_rc: $_cpl_scripts_dir"
    else
        printf '\n%s\n' "$_cpl_line" >> "$_cpl_rc"
        echo "Added permanently to $_cpl_rc: $_cpl_scripts_dir"
    fi
fi

if [ "$_cpl_sourced" -eq 0 ]; then
    echo "Note: script was run, not sourced; PATH of the current shell is unchanged." >&2
    echo "      Run: source $_cpl_self" >&2
fi

unset _cpl_permanent _cpl_arg _cpl_self _cpl_sourced _cpl_root _cpl_scripts_dir _cpl_rc _cpl_line
