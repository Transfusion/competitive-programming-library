import argparse, os
from pathlib import Path

BODY_FILE_PREFIX = "body"
OUTPUT_FILE_PREFIX = "output"

parser = argparse.ArgumentParser()
parser.add_argument("--lang", required=True, choices=["python", "cpp"])
# parser.add_argument("--all", action="store_true")
parser.add_argument(
    "--algos",
    nargs="+",
    help="List of directories to include; all if unspecified",
    required=False,
)
parsed_arguments = parser.parse_args()

exts = {"python": ".py", "cpp": ".cpp"}
ext = exts[parsed_arguments.lang.lower()]

current_file_name = Path(__file__).name

BODY_FILE_NAME = f"{BODY_FILE_PREFIX}{ext}"
OUTPUT_FILE_NAME = f"{OUTPUT_FILE_PREFIX}{ext}"

output = ""
for dirpath, dnames, fnames in os.walk("./"):
    for f in fnames:
        if f.endswith(ext) and f != current_file_name and f != BODY_FILE_NAME:
            print(f)
            # if algos is empty
            if not parsed_arguments.algos or any(
                algo in dirpath for algo in parsed_arguments.algos
            ):
                output += open(os.path.join(dirpath, f)).read() + "\n"

if os.path.isfile(BODY_FILE_NAME):
    output += open(os.path.join(BODY_FILE_NAME)).read()

f = open(OUTPUT_FILE_NAME, "w")
f.write(output)
f.close()
