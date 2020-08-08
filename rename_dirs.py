import os
import typing as t

# for d in os.listdir(os.getcwd()):
#     print(d)


# for i in os.listdir(os.getcwd()):
#     if i.startswith("."):
#         continue
#     new_dirname: str = f"Day{i}"
#     print(new_dirname)

# NOTE os.walk('.') -> (dirpath, dirnames, filenames) triple
DIRNAMES: int = 1
all_dirs: t.List[str] = next(os.walk("."))[DIRNAMES]
new_dirs: t.List[str] = []
# Specify what I want to add/remove etc.
text_to_add: str = "Day"

for d in all_dirs:
    # Check that dir doesn't already have prefix/text_to_add:
    if d.startswith(".") or d.startswith(text_to_add):
        continue
    new_dirname: str = f"{text_to_add}{d}"

    # Dry run:
    print(f"{new_dirname}\n{d}")

    # Perform the actual renaming:
    # os.rename(d, new_dirname)

    new_dirs.append(new_dirname)

print(new_dirs)
