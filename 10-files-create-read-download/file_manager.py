import os
import pathlib

# Absolute path (more stable)
this_file_path = os.path.abspath(__file__)
# print(this_file_path)
# /Users/gaylonalfano/Code/30-days-of-python/10-files-create-read-download/file_manager.py

# Create BASE_DIR (root) and PROJECT_DIR
BASE_DIR = os.path.dirname(this_file_path)  # 10-files-create-read-download
PROJECT_DIR = os.path.dirname(BASE_DIR)  # 30-days-of-python

# Join BASE_DIR with our actual file path
email_txt = os.path.join(BASE_DIR, "templates", "email.txt")


# # Relative path (can only run in 10-files dir)
# email_txt = os.path.join("templates", "some-sub-dir", "email.txt")
# # Testing out the new pathlib.Path() method
# email_content = pathlib.Path("templates") / "some-sub-dir" / "email.txt"

# print(f"email_txt:{email_txt}")
# print(f"email_content:{email_content}")


content = ""

with open(email_txt, "r") as f:
    content = f.read()

print(content.format(name="Archie"))
