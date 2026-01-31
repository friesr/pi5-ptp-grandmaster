import os
import time
import shutil

def get_directory_size_gb(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
            except FileNotFoundError:
                pass
    return total / (1024**3)

def list_files_sorted(path):
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(root, f)
            files.append((fp, os.path.getmtime(fp)))
    return sorted(files, key=lambda x: x[1])

def enforce_local_limit(path, max_gb):
    """Delete oldest files until local storage is under limit."""
    current = get_directory_size_gb(path)
    if current <= max_gb:
        return 0

    files = list_files_sorted(path)
    removed = 0

    for fp, _ in files:
        try:
            os.remove(fp)
            removed += 1
        except FileNotFoundError:
            pass

        current = get_directory_size_gb(path)
        if current <= max_gb:
            break

    return removed

def move_oldest_to_archive(local_path, archive_path, max_archive_gb):
    """Move oldest files from local to archive until archive is under limit."""
    archive_size = get_directory_size_gb(archive_path)
    if archive_size > max_archive_gb:
        return 0

    files = list_files_sorted(local_path)
    moved = 0

    for fp, _ in files:
        rel = os.path.relpath(fp, local_path)
        dest = os.path.join(archive_path, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        try:
            shutil.move(fp, dest)
            moved += 1
        except FileNotFoundError:
            pass

        archive_size = get_directory_size_gb(archive_path)
        if archive_size > max_archive_gb:
            break

    return moved
