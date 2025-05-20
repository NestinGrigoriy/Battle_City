import os
import pickle
from typing import Any


def load_data() -> dict[str, Any] | None:
    """Загружает сохраненный файл"""
    if not os.path.exists("savegame.pkl"):
        return None

    if os.path.getsize("savegame.pkl") == 0:
        return None

    with open("savegame.pkl", "rb") as f:
        try:
            data = pickle.load(f)
            if isinstance(data, dict):
                return data
            else:
                return None
        except (pickle.PickleError, EOFError):
            return None
