import os
import shutil
import requests


def download_file(url: str, directory: str, fname: str = None):
    """
    Download images or files from specified URL and
    save in specified directory.
    """
    # Give user chance to rename filename
    if fname is None:
        # Update filename to use basename of URL
        fname = os.path.basename(url)

    dl_filepath: str = os.path.join(directory, fname)

    with requests.get(url, stream=True) as r:
        with open(dl_filepath, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return dl_filepath


def download_file_slower(url: str):
    """
    Slower download method that chunks data. Uses more memory
    but could be useful if dealing with very large files.
    """
    local_filename: str = url.split("/")[-1]

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()

    return local_filename
