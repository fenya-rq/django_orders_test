import shutil
from typing import Callable
from io import BytesIO

import pytest
from PIL import Image

from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management import call_command

_not_existing: int = 9999


@pytest.fixture(scope="class")
def create_mock_image():
    """
    Creates a mock image for testing purposes and saves it to storage.

    :return: The file path of the saved mock image.
    """
    image = Image.new("RGB", (600, 600), color="red")
    img_io = BytesIO()
    image.save(img_io, format="JPEG")
    img_io.seek(0)
    file_path = r"uploads/2024/10/14/test_image.jpg"
    file_name = default_storage.save(file_path, File(img_io, name="test_image.jpg"))
    yield file_name
    default_storage.delete(file_path)
    shutil.rmtree("./file_storage/media/uploads/")


@pytest.fixture
def load_fixture(db) -> Callable[[str], None]:
    """
    Loads a fixture file into the database.

    :param db: Database fixture to ensure access to the database.
    :return: A callable function to load a specific fixture file.
    """

    def _load_fixture(file_name: str) -> None:
        """
        Calls the loaddata management command to load a fixture.

        :param file_name: The name of the fixture file to load (without extension).
        """
        call_command("loaddata", f"fixtures/{file_name}.json")

    return _load_fixture
