# aCropalypse-JPEG-PoC

> so basically the pixel 7 pro, when you crop and save a screenshot, overwrites the image with the new version, but leaves the rest of the original file in its place

For JPEG, just to detect whether the cropped image is affected by aCropalypse is simple: if there are 2 `EOI` marker

To sanitize the cropped image is also simple: delete everything after the first `EOI` marker

To restore the missing part of the image, let's get more information about JPEG compression and format!

- JPEG uses `YCbCr` color space, `Y` is for brightness, `Cb` and `Cr` are for color information.
- A JFIF marker consists of two bytes: `FF` not followed by `00` or `FF`
- Compressed image data are between `SOS` and `EOI`

So, if there is the compressed image data (of the rest part of the cropped image), the missing part of the image can be restored.

# Use

`python3 acropalypse_JPEG_detection.py path/to/file.jpg`

# ref

[Exploiting aCropalypse: Recovering Truncated PNGs](https://www.da.vidbuchanan.co.uk/blog/exploiting-acropalypse.html)

[JPEG File Interchange Format](https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format)

[JPEG format](https://github.com/corkami/formats/blob/master/image/jpeg.md)

[acropalypse_detection.py](https://github.com/infobyte/CVE-2023-21036/blob/master/acropalypse_detection.py)

[acropalypse_matching_sha256.py](https://gist.github.com/DavidBuchanan314/93de9d07f7fab494bcdf17c2bd6cef02)
