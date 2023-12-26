from birdweb.models import BirdImage


def test_parse(test_image):
    record = BirdImage.from_path(test_image, family='Mimidae', order='Passeriformes', species='Brown Thrasher')
    assert record.date_taken.year == 2014
