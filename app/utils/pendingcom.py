from config import DATA_DIR
import json
import os

ITEM_FILE = DATA_DIR + "/item.json"


def save_pending_com(info_type: str, mode: str, info: dict) -> None:

    if os.path.isfile(ITEM_FILE):
        with open(ITEM_FILE, "r") as file:
            data = json.load(file)

        data["item_list"].append({
            "type": info_type,
            "mode": mode,
            "info": info
        })
    else:
        data = {
            "item_list": [
                {
                    "type": info_type,
                    "mode": mode,
                    "info": info
                }
            ]
        }

    with open(ITEM_FILE, "w") as file:
        json.dump(data, file, indent=2)
