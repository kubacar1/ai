"""
Tests automatic loading of motion module/animator pipeline
"""
import os
import torch

from datetime import datetime

from typing import Literal, Optional

from enfugue.util import logger, fit_image, profiler, image_from_uri
from enfugue.diffusion.manager import DiffusionPipelineManager
from enfugue.diffusion.invocation import LayeredInvocation
from enfugue.diffusion.constants import *
from enfugue.diffusion.util import Video, GridMaker

from PIL import Image

from pibble.util.log import DebugUnifiedLoggingContext

def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(here, "test-results", "dragnuwa")
    input_dir = os.path.join(here, "test-images")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with DebugUnifiedLoggingContext():
        manager = DiffusionPipelineManager()
        invocation = LayeredInvocation.assemble(
            seed=12345,
            layers = [
                {
                    "image": image_from_uri("file://" + os.path.join(input_dir, "nuwa.png")),
                    "visibility": "visible"
                }
            ],
            animation_frames=28,
            animation_engine="svd",
            motion_vectors=[
                [
                    {
                        "anchor": (x1, y1)
                    },
                    {
                        "anchor": (x2, y2)
                    }
                ]
                for ((x1, y1), (x2, y2)) in [
                    ((222, 55), (0, 0)),
                    ((519, 21), (575, 0)),
                    ((205, 197), (0, 319)),
                    ((527, 180), (575, 319))
                ]
            ]
        )
        result = invocation.execute(manager)
        # result['frames'] = interpolated video frames (if present)
        # result['images'] = animation image sequences
        Video(result.get("frames", result["images"])).save(
            os.path.join(output_dir, "output.gif"),
            overwrite=True,
            rate=8.0
        )

if __name__ == "__main__":
    main()
