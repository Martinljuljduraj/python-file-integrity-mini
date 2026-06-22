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
        print(f"Skipping {file_path}: {exc}")
        return None
    

    # except FileNotFoundError:
    #     print(f"File not found: {file_path}")
    #     return None
    # except PermissionError:
    #     print(f"Permission denied: {file_path}")
    #     return None
        

if __name__ == "__main__":
    print(hash_file(Path("sample_files/example.txt")))