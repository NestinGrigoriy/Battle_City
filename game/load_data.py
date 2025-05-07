import os
import pickle


def load_data() -> map or None:
    """Загружает сохраненный файл"""
    if not os.path.exists("savegame.pkl"):
        return None

    if os.path.getsize("savegame.pkl") == 0:
        return None
    with open("savegame.pkl", "rb") as f:
        data = pickle.load(f)
        return data
