"""Data models used by our webpage"""
from datetime import datetime
from typing import Optional
from os import PathLike

from pydantic import BaseModel, Field

from PIL import Image
from PIL import ExifTags


class BirdImage(BaseModel):
    """An image of the bird and all metadata we know about it"""

    # Physical path on the filesystem
    path: Optional[PathLike] = Field(description='Path to the file on a local file system')

    # Spatiotemporal details
    coordinate: Optional[tuple[float, float, Optional[float]]] = Field(
        None, description='GPS coordinates for the image (latitude, longitude, meters ASL)'
    )
    date_taken: datetime = Field(None, description='When the photo was taken')

    # Taxonomy
    order: str = Field(description='Order for the bird')
    family: str = Field(description='Family of the bird')
    species: Optional[str] = Field(None, description='Species of the bird, if applicable')

    @classmethod
    def from_path(cls, image_path: str, **kwargs):
        """Parse the metadata from an image file, use it to construct model

        Args:
            image_path: Path to the image file
        Raises:
            (UnidentifiedImageError) If the image fails to read
        Returns:
            An image record using the metadata extracted from this image
        """

        with Image.open(image_path) as im:
            # Determine the shot time
            exif = im.getexif()
            shot_time = datetime.strptime(exif[ExifTags.Base.DateTime], '%Y:%m:%d %H:%M:%S')

            # Get the GPS location, if known
            coordinate = None
            if ExifTags.IFD.GPSInfo in exif:
                gps_data = exif.get_ifd(ExifTags.IFD.GPSInfo)
                if ExifTags.GPS.GPSLatitude in gps_data:
                    coordinate = [
                        gps_data[ExifTags.GPS.GPSLatitude],
                        gps_data[ExifTags.GPS.GPSLongitude],
                        gps_data.get(ExifTags.GPS.GPSAltitude, None)
                    ]

                    # Convert the coordinates to degrees
                    for i, x in enumerate(coordinate[:2]):
                        coordinate[i] = float(x[0] + x[1] / 60 + x[2] / 3600)

        # Make the record
        return cls(
            path=image_path,
            date_taken=shot_time,
            coordinate=coordinate,
            **kwargs
        )
