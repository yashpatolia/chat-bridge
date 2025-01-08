import requests
import logging
from config import HYPIXEL_API_KEY

def get_skyblock_data(uuid: str) -> dict:
    data = requests.get(f"https://api.hypixel.net/v2/skyblock/profiles?uuid={uuid}&key={HYPIXEL_API_KEY}").json()
    logging.debug(f"GET https://api.hypixel.net/v2/skyblock/profiles")
    return data
