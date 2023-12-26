"""Retrieve the data we will be serving"""
from pathlib import Path
from functools import cache

from birdweb.models import BirdImage

_bird_data_path = Path(__file__).parents[1] / 'birdweb.json'


@cache
def load_data() -> list[BirdImage]:
    """Load the data we will be serving"""
    with _bird_data_path.open() as fp:
        return [BirdImage.model_validate_json(line) for line in fp]
