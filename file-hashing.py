import hashlib
import pathlib
from pathlib import Path

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
        

if __name__ == "__main__":
    print(hash_file(Path("sample_files/example.txt")))