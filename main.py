import sys
from pathlib import Path
import uuid
import shutil

from normalize import normalize


CATEGORIES = {"Audio": [".mp3", ".ogg", ".wav", ".amr"],
              "Documents": [".docx", ".doc", ".txt", ".pdf", ".xlsx", ".pptx"],
              "Images":[".jpeg", ".png", ".jpg", ".svg"],
              "Video":[".avi", ".mp4", ".mov", ".mkv"],
              "Archives":[".zip", ".gz", ".tar"]}


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        # print(f"Make {target_dir}")
        target_dir.mkdir()
    # print(path.suffix)
    # print(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
       new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)
    

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        print(item)
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def delete_empty_folders(path: Path) -> None:
    for folder in path.glob("**/*"):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()


def unpack_archive(path: Path) -> None:
    archive_dir = path.joinpath("archives")
    archive_dir.mkdir(exist_ok=True)

    for archive in path.glob("**/*.zip"):
        target_subdir = archive_dir / normalize(archive.stem)
        target_subdir.mkdir(exist_ok=True)  
        shutil.unpack_archive(str(archive), str(target_subdir))
        archive.unlink()

    for archive in path.glob("**/*.tar"):
        target_subdir = archive_dir / normalize(archive.stem)
        target_subdir.mkdir(exist_ok=True)  
        shutil.unpack_archive(str(archive), str(target_subdir))
        archive.unlink()

    for archive in path.glob("**/*.gz"):
        target_subdir = archive_dir / normalize(archive.stem)
        target_subdir.mkdir(exist_ok=True)  
        shutil.unpack_archive(str(archive), str(target_subdir))
        archive.unlink()
    

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos`n exists."
    
    
    sort_folder(path)
    unpack_archive(path)
    delete_empty_folders(path)
    
    return "All ok"


if __name__ == "__main__":
    print(main())