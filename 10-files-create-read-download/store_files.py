import os
import typing as t

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES_DIR = os.path.join(BASE_DIR, "images")

# if not os.path.exists(FILES_DIR):
#     print("This is not a valid path.")

# Alternative check that dir exists; if not creates it
os.makedirs(FILES_DIR, exist_ok=True)

my_images: t.List[int] = range(0, 12)

for i in my_images:
    fname = f"{i}.txt"
    # Get the file path for each file
    file_path = os.path.join(FILES_DIR, fname)

    # Check whether file path (i.e., the files) already exists.
    # Can skip it if so to avoid overwriting, etc.
    if os.path.exists(file_path):
        print(f"Skipped {fname}")
        continue

    # Write content to this specific file using context manager
    with open(file_path, "w") as f:
        f.write(f"Hello! My file path is: {file_path}")
