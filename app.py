import os
import argparse
import random
import string
from datetime import datetime, timedelta

import pymongo

SITE = "https://shortlink.com/"
STORE_TIME = 10

def create_short_url():
    characters = string.ascii_letters + string.digits
    short_url = "".join(random.choice(characters) for _ in range(5))
    return short_url

def connect_to_mongodb():
    client = pymongo.MongoClient(os.environ.get("DATABASE_PATH"))
    db = client.url_shortener_db
    collection = db.shortened_urls
    return collection

def insert_minified_url(url: str):
    collection = connect_to_mongodb()
    short_url_key = create_short_url()
    data = {"url_key": short_url_key,
            "url": url,
            "inserted": datetime.now()}
    collection.insert_one(data)
    short_url = SITE + short_url_key
    return short_url

def get_expanded_url(url: str):
    url_key = url.replace(SITE, '')
    collection = connect_to_mongodb()
    data = collection.find_one({"url_key": url_key})

    if data is None:
        return "There is no such shortened URL"

    current_time = datetime.now()
    some_time_ago = current_time - timedelta(seconds=STORE_TIME)

    if data['inserted'] < some_time_ago:
        return "URL has expired"
    else:
        return data['url']


def main():
    parser = argparse.ArgumentParser(description="App to create shortened URLs")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--minify", type=str, help="URL to shorten")
    group.add_argument("--expand", type=str, help="Option Bar")

    args = parser.parse_args()

    result = "No parameter were provided"

    if args.minify:
        result = insert_minified_url(args.minify)
    elif args.expand:
        result = get_expanded_url(args.expand)

    return print(result)


if __name__ == "__main__":
    main()
