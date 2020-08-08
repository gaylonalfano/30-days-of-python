import os

ABS_PATH: str = os.path.abspath(__file__)
BASE_DIR: str = os.path.dirname(ABS_PATH)  # 15-video-processing-moviepy
DATA_DIR: str = os.path.join(BASE_DIR, "data")
SAMPLE_DIR: str = os.path.join(DATA_DIR, "samples")
SAMPLE_INPUTS: str = os.path.join(SAMPLE_DIR, "inputs")
SAMPLE_OUTPUTS: str = os.path.join(SAMPLE_DIR, "outputs")
