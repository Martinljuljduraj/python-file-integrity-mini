import hashlib
import pathlib
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
    




if __name__ == "__main__":
    # testing for Milestone 1
    # print(hash_file(Path("sample_files/example.txt")))
    # testing for Milestone 2
    print(scan_directory(Path("sample_files"))) # tested and works as needed

    # baseline = scan_directory("./sample_files")
    # print(baseline)

