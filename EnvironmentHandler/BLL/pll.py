from dal import *
from datetime import datetime, time


class PlantLogic:

    def __init__(self):
        self.data_access = DataAccess()

    def commit_measurement(
            self, plant_id: int, water: int, temperature: float, humidity: int, light: int, moisture: int)\
            -> Tuple[bool, int]:
        light_mmol = int(round(light / 54 * 3600 / 1000))
        self.data_access.save_measurement(plant_id, water, temperature, humidity, light_mmol, moisture)
        plant_data = self.data_access.get_plant_data(plant_id)
        collected_light = self.data_access.get_todays_light_exposure(plant_id)

    def configure(self, mac_address: str) -> int:
        return self.data_access.configure(mac_address)
