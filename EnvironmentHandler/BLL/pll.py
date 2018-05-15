from DAL import dal
from dal import DataAccess
from datetime import time
from estimator import Estimator
import numpy as np
from typing import Tuple


class PlantLogic:

    def __init__(self):
        self.data_access = DataAccess()
        self.estimator = Estimator()

    def commit_measurement(
            self, plant_id: int, water: int, temperature: float, humidity: int, light: int, moisture: int)\
            -> Tuple[bool, int]:
        light_mmol = int(round(light / 54 * 3600 / 1000))
        self.data_access.save_measurement(plant_id, water, temperature, humidity, light_mmol, moisture)
        plant_data = self.data_access.get_plant_data(plant_id)
        collected_light = self.data_access.get_todays_light_exposure(plant_id)
        light_on = False
        water_time = 0
        if plant_data.dark_hours_start > time() > plant_data.dark_hours_end:
            estimated_total_light = self.estimator.estimate_total_light(collected_light, plant_data.dark_hours_start)
            if estimated_total_light < plant_data.light_low:
                light_on = True
        if plant_data.silent_hours_start > time() > plant_data.silent_hours_end:
            if moisture < plant_data.moisture_low + 10:
                water_time = (((plant_data.pot_size / 2) ** 2 * np.pi * 0.04) / 280) * 3600
        return light_on, water_time

    def configure(self, mac_address: str) -> int:
        return self.data_access.configure(mac_address)

    def get_plants(self):
        return self.data_access.get_plants()

    def get_history(self):
        return self.data_access.get_history()

    def get_settings(self, plant_id: int):
        return self.data_access.get_settings(plant_id)

    def post_settings(self):
        return self.post_settings()
