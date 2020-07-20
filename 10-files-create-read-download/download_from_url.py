import os
import sys
import typing as t
import getopt

from download_util import download_file

# Construct absolute path for downloaded files
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DEST_DIR: str = os.path.join(BASE_DIR, "downloads")
os.makedirs(DEFAULT_DEST_DIR, exist_ok=True)

# Get a random image address with file extension
DEFAULT_URL: str = "https://upload.wikimedia.org/wikipedia/commons/1/1c/Sevan_Armenia_%D0%A1%D0%B5%D0%B2%D0%B0%D0%BD_%D0%90%D1%80%D0%BC%D0%B5%D0%BD%D0%B8%D1%8F.jpeg"

# TODO: 2020/07/20 - Fix directory arg. Consider put constants in function

# Give user option to pass command args when calling this module
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def download_from_url(argv: t.List[str]):
    """
    Main module function that accepts command-line arguments and
    downloads a single file from specified url.

    The command-line arguments are passed to a 'download_file'
    utility function.
    """
    url: str = DEFAULT_URL
    directory: str = DEFAULT_DEST_DIR
    filename: str = None

    try:
        opts, args = getopt.getopt(argv, "hu:d:f:", ["url=", "dir=", "fname="])
    except getopt.GetoptError:
        print(
            f"GetoptError: \n{os.path.basename(os.path.abspath(__file__))} -u <url> -d <directory> -f <filename>"
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print(
                f"usage: {os.path.basename(os.path.abspath(__file__))} -u <url> -d <directory> -f <filename>"
            )
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-d", "--directory"):
            directory = arg
        elif opt in ("-f", "--filename"):
            filename = arg

    # Call our util function download_file with these updated args
    dl_filepath: str = download_file(url, directory, filename)

    print(f"Number of args passed: {len(argv)} arguments.")
    print(f"url: {url}")
    print(f"directory: {directory}")
    print(f"filename: {filename}")
    print(f"Final download filepath: {dl_filepath}")


if __name__ == "__main__":
    download_from_url(sys.argv[1:])

# if __name__ == "__main__":
#     print(f"Number of args: {len(sys.argv)} arguments.")
#     print(f"Argument list: {str(sys.argv)})")

#     # sys.argv -> script_name, url, directory, filename
#     url: str = DEFAULT_URL
#     if len(sys.argv) > 1:
#         url = sys.argv[1]

#     directory: str = DOWNLOADS_DIR
#     if len(sys.argv) > 2:
#         directory = sys.argv[2]

#     filename: str = None
#     if len(sys.argv) > 3:
#         filename = sys.argv[3]

#     downloaded_file = download_file(url, directory, filename)
#     print(f"Download saved in: {downloaded_file}")
