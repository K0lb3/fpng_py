from enum import IntEnum

from ._fpng_py import *

class CompressionFlags(IntEnum):
    """
    Enables computing custom Huffman tables for each file, instead of using the custom global tables.
    Results in roughly 6% smaller files on average, but compression is around 40% slower.
    FPNG_ENCODE_SLOWER = 1,

    Only use raw Deflate blocks (no compression at all). Intended for testing.
    FPNG_FORCE_UNCOMPRESSED = 2,
    """

    NONE = 0
    FPNG_ENCODE_SLOWER = 1
    FPNG_FORCE_UNCOMPRESSED = 2
