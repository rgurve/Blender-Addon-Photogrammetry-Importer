import os
from photogrammetry_importer.utility.blender_logging_utility import log_report

try:
    from PIL import Image as _PILImage
except ImportError:
    _PILImage = None


class ImageFileHandler:
    """Class to read and write images using :code:`Pillow`."""

    @staticmethod
    def read_image_size(image_ifp, default_width, default_height, op=None):
        """Read image size from disk."""

        if _PILImage is not None and os.path.isfile(image_ifp):
            # This does NOT load the data into memory -> should be fast!
            image = _PILImage.open(image_ifp)
            width, height = image.size
            success = True
        elif default_width > 0 and default_height > 0:
            width = default_width
            height = default_height
            log_report(
                "WARNING",
                "Set width and height to provided default values! ("
                + str(default_width)
                + ", "
                + str(default_height)
                + ")",
                op,
            )
            success = True
        else:
            if _PILImage is None:
                log_report(
                    "ERROR",
                    "PIL/PILLOW is not installed. Can not read image from disc"
                    + " to get image size.",
                    op,
                )
            else:
                log_report(
                    "ERROR",
                    "Corresponding image not found at: " + image_ifp,
                    op,
                )
            log_report(
                "ERROR",
                "Invalid default values provided for width ("
                + str(default_width)
                + ") and height ("
                + str(default_height)
                + ")",
                op,
            )
            if _PILImage is None:
                log_report(
                    "ERROR",
                    "Adjust the default width/height values to import the"
                    + " NVM / LOG / MVE file.",
                    op,
                )
            else:
                log_report(
                    "ERROR",
                    "Adjust the image path or the default width/height values"
                    + " to import the NVM / LOG file.",
                    op,
                )
            width = None
            height = None
            success = False
        return success, width, height
