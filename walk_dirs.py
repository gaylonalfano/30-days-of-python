import os

# path_to_walk: str = os.chdir("/Users/gaylonalfano/Code/dotfiles")

# for dirpath, dirnames, filenames in os.walk(os.getcwd()):
#     print(f"Current path: {dirpath}")
#     print(f"Directories: {dirnames}")
#     print(f"Files: {filenames}\n")


# To walk only top-level directories
DIRNAMES = 1
print(next(os.walk(os.getcwd()))[DIRNAMES])
