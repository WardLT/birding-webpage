from pathlib import Path
from shutil import copy

from pytest import fixture

from birdweb.index import index_images, cli_main


@fixture
def indexable_dir(test_image, tmpdir):
    # Make the directory
    species_dir = Path(tmpdir) / 'Passeriformes' / 'Mimidae' / 'Brown Thrasher'
    species_dir.mkdir(parents=True)

    # Add the test image and a non-image file
    copy(test_image, species_dir / 'Adult, 4-14.jpg')
    (species_dir / 'test.txt').write_text('Nope')

    return tmpdir


def test_index(indexable_dir):
    record = next(index_images(indexable_dir))
    assert record.species == 'Brown Thrasher'
    assert record.family == 'Mimidae'
    assert record.order == 'Passeriformes'


def test_cli(indexable_dir, tmpdir, capsys):
    output_path = Path(tmpdir) / 'birds.json'
    cli_main(['--output-path', str(output_path), str(indexable_dir)])
    assert output_path.stat().st_size > 0
