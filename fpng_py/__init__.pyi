from typing import Tuple

from . import CompressionFlags

# FUNCTION STUBS

def fpng_cpu_supports_sse41() -> bool:
    """
    Returns true if the CPU supports SSE 4.1, and SSE support wasn't disabled by setting FPNG_NO_SSE=1.
    """
    raise NotImplementedError()


def fpng_crc32(data: bytes, prev_crc32: int = 0) -> int:
    """
    Computes the CRC32 of the given data.
    Fast CRC-32 SSE4.1+pclmul or a scalar fallback (slice by 4)

    Parameters
    ----------
    data : bytes
        The data to compute the CRC32 of.
    prev_crc32 : int, optional
        The previous CRC32 value. Defaults to 0.
    """
    raise NotImplementedError()


def fpng_adler32(data: bytes, adler: int = 1):
    """
    Computes the Adler32 of the given data.
    Fast Adler32 SSE4.1 Adler-32 with a scalar fallback.

    Parameters
    ----------
    data : bytes
        The data to compute the Adler32 of.
    adler : int, optional
        The previous Adler32 value. Defaults to 1.
    """
    raise NotImplementedError()


def fpng_encode_image_to_memory(
    image: bytes,
    width: int,
    height: int,
    num_channels: int = 0,
    flags: CompressionFlags = CompressionFlags.NONE,
) -> bytes:
    """
    Encodes the given image into a PNG file in memory.
    Fast PNG encoding. The resulting file can be decoded either using a standard PNG decoder or by the fpng_decode_memory() function below.

    Parameters
    ----------
    image : bytes
        binary data of RGB or RGBA image pixels, R first in memory, B/A last.
    width: int
        width of the image
    height: int
        height of the image
    num_channels: int, optional
        number of channels in the image, 3 for RGB, 4 for RGBA
        if num_chans is 0, it will be inferred from the image data.
        image's row pitch in bytes must is w*num_chans.
    flags: CompressionFlags, optional
        flags for the encoder. Defaults to 0.
    """
    raise NotImplementedError()


def fpng_encode_image_to_file(
    filename: str,
    image: bytes,
    width: int,
    height: int,
    num_channels: int = 0,
    flags: CompressionFlags = CompressionFlags.NONE,
) -> None:
    """
    Encodes the given image into a PNG file.
    Fast PNG encoding. The resulting file can be decoded either using a standard PNG decoder or by the fpng_decode_memory() function below.

    Parameters
    ----------
    filename : str
        path to the file to write the PNG to.
    image : bytes
        binary data of RGB or RGBA image pixels, R first in memory, B/A last.
    width: int
        width of the image
    height: int
        height of the image
    num_channels: int, optional
        number of channels in the image, 3 for RGB, 4 for RGBA
        if num_chans is 0, it will be inferred from the image data.
        image's row pitch in bytes must is w*num_chans.
    flags: CompressionFlags, optional
        flags for the encoder. Defaults to 0.
    """
    raise NotImplementedError()


def fpng_get_info(image: bytes) -> Tuple[int, int, int]:
    """
    Returns the width, height and number of channels of the given image.
    Fast PNG decoding of files ONLY created by fpng_encode_image_to_memory() or fpng_encode_image_to_file().
    If fpng_get_info() or fpng_decode_memory() returns FPNG_DECODE_NOT_FPNG, you should decode the PNG by falling back to a general purpose decoder.
    fpng_get_info() parses the PNG header and iterates through all chunks to determine if it's a file written by FPNG, but does not decompress the actual image data so it's relatively fast.

    Parameters
    ----------
    image : bytes
        binary data of RGB or RGBA image pixels, R first in memory, B/A last.

    Returns
    -------
    (width, height, num_chans) : Tuple[int, int, int]
    """
    raise NotImplementedError()


def fpng_decode_from_memory(
    image: bytes, desired_channels: int
) -> Tuple[bytes, int, int, int]:
    """
    Decodes the given image from memory.
    fpng_decode_memory decompresses 24/32bpp PNG files ONLY encoded by this module.
    If the image is 24bpp and 32bpp is requested, the alpha values will be set to 0xFF.
    If the image is 32bpp and 24bpp is requested, the alpha values will be discarded.

    Parameters
    ----------
    image : bytes
        binary data of RGB or RGBA image pixels, R first in memory, B/A last.
    desired_channels : int
        number of channels to decode the image to.
        3 for RGB, 4 for RGBA

    Returns
    -------
    (image, width, height, num_chans) : Tuple[bytes, int, int, int]
    """
    raise NotImplementedError()


def fpng_decode_from_file(
    filename: str, desired_channels: int
) -> Tuple[bytes, int, int, int]:
    """
    Decodes the given image from a file.

    fpng_decode_file decompresses 24/32bpp PNG files ONLY encoded by this module.
    If the image is 24bpp and 32bpp is requested, the alpha values will be set to 0xFF.
    If the image is 32bpp and 24bpp is requested, the alpha values will be discarded.

    Parameters
    ----------
    filename : str
        path to the file to decode.
    desired_channels : int
        number of channels to decode the image to.
        3 for RGB, 4 for RGBA

    Returns
    -------
    (image, width, height, num_chans) : Tuple[bytes, int, int, int]
    """
    raise NotImplementedError()
