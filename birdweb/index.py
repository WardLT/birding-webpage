"""Index a directory of bird photos"""
from typing import Iterator
from pathlib import Path

from PIL import UnidentifiedImageError

from .models import BirdImage


def index_images(file_path: str) -> Iterator[BirdImage]:
    """Parse a series of records from a filesystem organized by order, family, and species.

    Args:
        Path to the root folder containing the images
    Yields:
        A record describing each image
    """

    # The folders are nested "order/family/species"
    for order_path in Path(file_path).iterdir():
        if not order_path.is_dir():
            continue
        for family_path in order_path.iterdir():
            if not family_path.is_dir():
                continue
            for species_path in family_path.iterdir():
                for file_path in species_path.iterdir():
                    try:
                        yield BirdImage.from_path(
                            file_path,
                            order=order_path.name,
                            family=family_path.name,
                            species=species_path.name
                        )
                    except UnidentifiedImageError:
                        continue
