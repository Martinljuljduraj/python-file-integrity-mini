import hashlib
import pathlib
import json
import argparse
from pathlib import Path
from datetime import datetime

# Milestone 1
def hash_file(file_path: Path) -> str:
    # calculate the hash of a file using SHA256
    h = hashlib.sha256() 

    CHUNK = 8192
    try:
        with open (file_path, "rb") as f:
            for chunk in iter(lambda: f.read(CHUNK), b""):
                h.update(chunk)
        return h.hexdigest()
    except (FileNotFoundError, PermissionError) as exc:
        print(f"Skipping {file_path}: {exc}") # Wrote skipping since we know there is a file to go to in our case
        return None
    


# Milestone 2
def scan_directory(directory: Path) -> dict:
    # ignore all these folders
    ignored_folders = {".git", "venv", "__pycache__", "node_modules"}

    root = Path(directory).resolve()  # Convert to absolute path first
    files_data = {} # our dict
    

    for p in root.rglob("*"):
        if not p.is_file(): # checking if it is a file
            continue
        if any(part in ignored_folders for part in p.parts): # skip anything inside ignored_folders
            continue
        
        # Turn each absolute path into a path relative to the scan root.
        rel = p.relative_to(root).as_posix()
        file_stat = p.stat()
        file_hash = hash_file(p)

        files_data[rel] = {
            "hash": file_hash,
            "size": file_stat.st_size,
            "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }
    
    return files_data


# Milestone 3
def save_baseline(scan_results: dict, output_path: Path, root_path: Path) -> None:
    # create output folder if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # build the wrapper dict
    # use the actual values and do not hardcode
    baseline = {
        "created_at": datetime.now().isoformat(),
        "root_path": root_path.as_posix(),
        "files": scan_results
    }

    # write to JSON file
    with open(output_path, "w") as f:
        json.dump(baseline, f, indent=4)

# Continuing Milestone 3 outside of any functions
# Here goes the argparse part as it is needed to run the example command:
# python3 fim.py baseline --path ./sample_files --output ./baselines/baseline.json
parser = argparse.ArgumentParser(description="File Integrity Monitor")
subparsers = parser.add_subparsers(dest="command")

baseline_parser = subparsers.add_parser("baseline")
baseline_parser.add_argument("--path", required=True)
baseline_parser.add_argument("--output", required=True)




if __name__ == "__main__":
    # testing for Milestone 1
    # print(hash_file(Path("sample_files/example.txt")))
    # testing for Milestone 2
    # print(scan_directory(Path("sample_files"))) # tested and works as needed
    # testing for Milestone 3 - printing this straight up won't appear the way it does from baseline.json as intended
    # results = scan_directory(Path("sample_files"))
    # save_baseline(results, Path("baselines/baseline.json"), Path("sample_files"))
    # Parsing gave me a much cleaner way to test if we see if baseline (.json) is saved to the baselines folder
    args = parser.parse_args()
    if args.command == "baseline":
        results = scan_directory(Path(args.path))
        save_baseline(results, Path(args.output), Path(args.path))
        print(f"Baseline saved to {args.output}")
    


    # baseline = scan_directory("./sample_files")
    # print(baseline)

