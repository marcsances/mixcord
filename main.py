import json
import time
from datetime import datetime

import requests
from config import *


def calc_length(length: int) -> str:
    hours = str(int(length / 3600)) + ":"
    if length < 3600:
        hours = ""
    minutes = str(int(length % 3600 / 60)).zfill(2)
    seconds = str(int(length % 3600 % 60)).zfill(2)
    return f"{hours}{minutes}:{seconds}"


def do_notify(key: str):
    metadata = requests.get(f"https://api.mixcloud.com{key}").json()
    payload = {
        "content": PO_NEW_SHOW,
        "embeds": [
            {
                "title": metadata["name"] if "name" in metadata else "",
                "description": metadata["description"] if "description" in metadata else "",
                "url": metadata["url"] if "url" in metadata else f"https://mixcloud.com{key}",
                "color": int(metadata["picture_primary_color"], 16) if "picture_primary_color" in metadata else 0,
                "fields": [
                    {
                        "name": "Tags",
                        "value": ", ".join(map(lambda t: t["name"], metadata["tags"] if "tags" in metadata else []))
                    },
                    {
                        "name": "Show length",
                        "value": calc_length(metadata["audio_length"]) if "audio_length" in metadata else "Unknown"
                    }
                ],
                "author": {
                    "name": MIXCLOUD_USER,
                    "url": f"https://www.mixcloud.com/{MIXCLOUD_USER}",
                    "icon_url": metadata["user"]["pictures"]["small"] if "user" in metadata and "pictures" in metadata["user"] and "small" in metadata["user"]["pictures"] else None
                },
                "footer": {
                    "text": "Mixcloud",
                },
                "timestamp": metadata["created_time"] if "created_time" in metadata else datetime.now().isoformat(),
                "thumbnail": {
                    "url": metadata["pictures"]["medium"] if "pictures" in metadata and "medium" in metadata["pictures"] else None
                }
            }
        ]
    }
    requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json;charset=UTF-8"})
    time.sleep(2)


def main():
    try:
        with open("known.shows", "r") as f:
            known_shows = f.read().split("\n")
    except IOError:
        known_shows = []

    feed = requests.get(f"https://api.mixcloud.com/{MIXCLOUD_USER}/cloudcasts/").json()
    for cloudcast in feed["data"]:
        if cloudcast["key"] not in known_shows:
            do_notify(cloudcast["key"])
            known_shows.append(cloudcast["key"])

    with open("known.shows", "w") as f:
        f.write("\n".join(known_shows))


if __name__ == "__main__":
    main()
