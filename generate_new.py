import argparse, os, sys
from pathlib import Path

# from parser import CPPParser

from amalgamater import CPPAmalgamater, PythonAmalgamater

from file_walker import walk
from import_replacer import replace

parser = argparse.ArgumentParser()
parser.add_argument(
    "--main",
    # nargs="+",
    help="The main file",
    required=True,
)

parsed_arguments = parser.parse_args()

_, extension = os.path.splitext(parsed_arguments.main)

amalgamater = None

match extension:
    case ".cpp":
        amalgamater = CPPAmalgamater()
    case ".py":
        amalgamater = PythonAmalgamater()

# imports_to_replace = walk(parsed_arguments.main, parser)
# replaced_output = replace(open(os.path.join(parsed_arguments.main)).read(), imports_to_replace)

# Sources are UTF-8; without this, redirected stdout on Windows uses the locale codepage (e.g. cp1252).
sys.stdout.reconfigure(encoding="utf-8")
print(amalgamater.amalgamate(parsed_arguments.main))
