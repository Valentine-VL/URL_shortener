from datetime import datetime, timedelta
from unittest.mock import patch

import mongomock
import pytest
from bson.objectid import ObjectId

from app import create_short_url, get_expanded_url


def test_create_short_url():
    short_url = create_short_url()
    assert len(short_url) == 5
    assert short_url.isalnum()

@pytest.mark.parametrize("key,url,date", [
    ("aaaaa", "https://example1.com/", datetime(2023, 1, 1, 0, 0, 0)),
    ("bbbbb", "https://example2.com/", datetime.now()),
])
def test_insert_minified_url(key, url, date):
    collection = mongomock.Connection().test_db.test_collection

    insert_data = {
        "url_key": key,
        "url": url,
        "inserted": date,
    }
    inserted_id = collection.insert(insert_data)
    # assert ObjectId(inserted_id).is_valid
    assert type(inserted_id) == type(ObjectId())

@pytest.mark.parametrize("key,url,time,expected", [
    ("aaaaa","https://example1.com/", datetime.now(), "https://example1.com/"),
    ("some_key", None, None,  "There is no such shortened URL"),
    ("ccccc", "https://example3.com/", datetime.now() - timedelta(seconds=11), "URL has expired")])
def test_get_expanded_url(key, url, time, expected):

    expected_obj = {
        "url_key": key,
        "url": url,
        "inserted": time,
    } if not url is None else None

    with patch("pymongo.collection.Collection.find_one", return_value=expected_obj):
        result = get_expanded_url("https://shortlink.com/" + key)

    expected_output = expected
    assert result == expected_output


if __name__ == "__main__":
    pytest.main()
