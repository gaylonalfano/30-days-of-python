import os
import typing as t

import numpy as np
from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import VideoFileClip  # Or, *
from PIL import Image

"""
NOTES:
    - conf.py is just like settings.py basically
    - Can run 'inference' computer vision machine learning on frames (ndarray)
    - Use pillow to convert each frame into its own image by converting
      numpy array into single image.
"""


# Path to video file
source_path = os.path.join(SAMPLE_INPUTS, "sample.mp4")
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-frame")
os.makedirs(thumbnail_dir, exist_ok=True)
os.makedirs(thumbnail_per_frame_dir, exist_ok=True)

# Save a clip
clip = VideoFileClip(source_path)
# print(type(clip.reader.fps))  # float
# print(type(clip.reader.nframes))  # int
# print(type(clip.duration))  # float seconds
duration: float = clip.reader.duration

# Convert each frame into an image using duration
for i in range(0, round(duration + 1)):
    frame: "np.ndarray[np.int]" = clip.get_frame(int(i))  # Need an int
    # print(type(frame))  # np.ndarray
    # print(frame.shape)  # (1080, 1920, 3)
    # Use Pillow (PIL) Image class to convert np.ndarray to image
    new_image = Image.fromarray(frame)
    # Assign a filepath for this new_image
    new_image_filepath: str = os.path.join(thumbnail_dir, f"{i}.jpg")
    new_image.save(new_image_filepath)
    print(f"Frame at { i } seconds. Image saved at: {new_image_filepath}")

fps: float = clip.reader.fps
nframes: int = clip.reader.nframes
seconds: float = nframes / (fps * 1.0)

# Convert each frame into an image using iter_frames()
for frame_index, frame in enumerate(clip.iter_frames()):
    # print(type(frame))  # np.ndarray
    # print(frame.shape)  # (1080, 1920, 3)
    if frame_index % fps == 0:
        current_milliseconds: int = int((frame_index / fps) * 1000)
        # Use Pillow (PIL) Image class to convert np.ndarray to image
        new_image = Image.fromarray(frame)
        # Assign a filepath for this new_image
        new_image_filepath: str = os.path.join(
            thumbnail_per_frame_dir, f"{i}.jpg"
        )
        new_image.save(new_image_filepath)
    print(f"Frame at { i } seconds. Image saved at: {new_image_filepath}")
