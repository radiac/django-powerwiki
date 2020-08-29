import pytest
from model_bakery import baker

from powerwiki.models import Asset, Page, Wiki


@pytest.fixture
def wiki(db):
    return baker.make(Wiki, slug="slug")


@pytest.fixture
def page(db, wiki):
    return baker.make(Page, wiki=wiki, path="parent/page")


@pytest.fixture
def asset(db, wiki):
    return baker.make(Asset, wiki=wiki, name="image", _create_files=True)
