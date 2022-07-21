from io import BytesIO
import os
from time import time_ns

from PIL import Image

# stupid bypass to force the import of the site-lib fpng_py
import sys
syspath = sys.path
sys.path = [path for path in sys.path if path.strip('.')]
from fpng_py import *
sys.path = syspath


LOCAL = os.path.dirname(os.path.realpath(__file__))
SAMPLE_FP = os.path.join(LOCAL, "example.png")
SAMPLE_IMAGE = Image.open(SAMPLE_FP)


def test_fpng_cpu_supports_sse41():
    print(fpng_cpu_supports_sse41())


def test_fpng_encode_img():
    fpng_data = fpng_encode_image_to_memory(
        SAMPLE_IMAGE.tobytes(),
        SAMPLE_IMAGE.width,
        SAMPLE_IMAGE.height,
        0,
        CompressionFlags.NONE,
    )
    fpng_img = Image.open(BytesIO(fpng_data))
    # RGB(A) check
    assert fpng_img.tobytes() == SAMPLE_IMAGE.tobytes()


def test_fpng_decode_img():
    fpng_data = fpng_encode_image_to_memory(
        SAMPLE_IMAGE.tobytes(),
        SAMPLE_IMAGE.width,
        SAMPLE_IMAGE.height,
        CompressionFlags.NONE,
    )
    dec_rgb, width, height, channels = fpng_decode_from_memory(
        fpng_data, len(SAMPLE_IMAGE.getbands())
    )
    assert width == SAMPLE_IMAGE.width
    assert height == SAMPLE_IMAGE.height
    dec_img = Image.frombytes("RGB", (SAMPLE_IMAGE.width, SAMPLE_IMAGE.height), dec_rgb)
    # RGB(A) check
    assert dec_img.tobytes() == SAMPLE_IMAGE.tobytes()


def benchmark():
    # benchmark
    compression_levels = range(0, 10)
    for level in compression_levels:
        times = []
        sizes = []
        for i in range(3):
            t1 = time_ns()
            stream = BytesIO()
            SAMPLE_IMAGE.save(stream, "PNG", compress_level=level)
            data = stream.getvalue()
            t2 = time_ns()
            times.append(t2 - t1)
            sizes.append(stream.tell())
        print(f"Level: {level}")
        print(f"  Size: {sum(sizes)/3}")
        print(f"  Time: {sum(times)/3}")

    times = []
    sizes = []
    rgb_data = SAMPLE_IMAGE.tobytes()
    width, height = SAMPLE_IMAGE.size
    for i in range(3):
        t1 = time_ns()
        d = fpng_encode_image_to_memory(rgb_data, width, height, 3)
        t2 = time_ns()
        times.append(t2 - t1)
        sizes.append(len(d))
    print("fpng")
    print(f"  Size: {sum(sizes)/3}")
    print(f"  Time: {sum(times)/3}")


if __name__ == "__main__":
    test_fpng_cpu_supports_sse41()
    test_fpng_encode_img()
    test_fpng_decode_img()
    benchmark()
