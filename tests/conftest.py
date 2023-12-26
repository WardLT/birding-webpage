from pathlib import Path

from pytest import fixture


@fixture()
def file_dir():
    return Path(__file__).parent / 'files'


@fixture()
def test_image(file_dir):
    return file_dir / 'test-image.jpg'
