def get_slayers(skyblock_data: dict, uuid: str) -> str:
    slayers: str = ""

    for profile in skyblock_data['profiles']:
        if skyblock_data['profiles'][profile]['selected'] is True:
            for slayer_name, values in skyblock_data['profiles'][profile]['members'][uuid]['slayer'].items():
                slayer_level = skyblock_data['profiles'][profile]['members']['uuid']['slayer'][slayer_name]['claimed_levels'].keys()[-1][-1]
                slayers += f"{slayer_level}/"

    return slayers[:-1]
