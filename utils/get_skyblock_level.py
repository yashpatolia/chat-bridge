import logging

def get_skyblock_level(skyblock_data: dict, uuid: str) -> float:
    skyblock_level: float = 0

    for profile in skyblock_data['profiles']:
        try:
            level: float = skyblock_data['profiles'][profile]['members'][uuid]['leveling']['experience'] / 100
            skyblock_level = level if level > skyblock_level else skyblock_level
        except Exception as e:
            logging.error(e)

    return skyblock_level
