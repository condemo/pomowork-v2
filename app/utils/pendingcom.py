from config import DATA_DIR
import json


def save_pending_com(info_type: str, mode: str, info: dict) -> None:
    data = {
        "type": info_type,
        "mode": mode,
        "info": info
    }
    with open(DATA_DIR + "/item.json", "w") as file:
        json.dump(data, file, indent=2)
