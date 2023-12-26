"""Index a directory of bird photos"""
from argparse import ArgumentParser
from typing import Iterator, Optional
from pathlib import Path
from time import monotonic
import logging
import sys

from PIL import UnidentifiedImageError

from .models import BirdImage

logger = logging.getLogger(__name__)


def index_images(file_path: str) -> Iterator[BirdImage]:
    """Parse a series of records from a filesystem organized by order, family, and species.

    Args:
        Path to the root folder containing the images
    Yields:
        A record describing each image
    """

    # The folders are nested "order/family/species"
    for order_path in Path(file_path).iterdir():
        if not order_path.is_dir() or not order_path.name.endswith('formes'):
            continue
        for family_path in order_path.iterdir():
            if not family_path.is_dir():
                continue
            for species_path in family_path.iterdir():
                if not species_path.is_dir():
                    continue
                for file_path in species_path.iterdir():
                    try:
                        yield BirdImage.from_path(
                            file_path,
                            order=order_path.name,
                            family=family_path.name,
                            species=species_path.name
                        )
                    except (UnidentifiedImageError, KeyError):
                        continue


def cli_main(args: Optional[list[str]] = None):
    """Run indexing and save to disk"""

    # Determine where to index
    parser = ArgumentParser()
    parser.add_argument('index_dir', help='Directory to be indexed')
    parser.add_argument('--output-path', help='Path in which to store output file', default='birdweb.json')
    parser.add_argument('--log-frequency', default=100, type=int, help='How often to report progress')
    args = parser.parse_args(args)

    # Start logging
    handlers = [logging.StreamHandler(sys.stdout)]
    for handler in handlers:
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    for logger_name in ['birdweb']:
        my_logger = logging.getLogger(logger_name)
        for handler in handlers:
            my_logger.addHandler(handler)
        my_logger.setLevel(logging.INFO)

    # Run the indexing
    logger.info(f'Reading from {args.index_dir} writing to {args.output_path}')
    start_time = monotonic()
    with open(args.output_path, 'w') as fp:
        for i, record in enumerate(index_images(args.index_dir)):
            print(record.model_dump_json(), file=fp)
            if i > 0 and i % args.log_frequency == 0:
                logger.info(f'Finished processing record {i + 1}. Species: {record.species}.'
                            f' Process rate: {(i + 1) / (monotonic() - start_time):.1f} records/s')

    # Report completion
    run_time = monotonic() - start_time
    logger.info(f'Processed {i + 1} records. Rate: {(i + 1) / run_time:.2f} records/s')
