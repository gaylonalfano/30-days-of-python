import os

os.chdir("/path/to/dir")

for f in os.listdir(os.getcwd()):
    # How to add type hints w/ tuple extraction?
    # f_name: str, f_ext: str = os.path.splitext(f)
    # f_title: str, f_course: str, f_num: str = f_name.split('-')
    f_name, f_ext = os.path.splitext(f)
    f_title, f_course, f_num = f_name.split("-")

    f_title = f_title.strip()
    f_course = f_course.strip()
    f_num = f_num.strip()[1:].zfill(2)  # turn to two digit num

    new_name: str = f"{f_num}-{f_title}{f_ext}"
