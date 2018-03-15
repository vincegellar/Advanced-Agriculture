from DAL import dal
from dal import *


class PlantLogic:

    def __init__(self):
        self.data_access = DataAccess()

    def save_measurement(self, plant_id, water, temperature, humidity, light, moisture):
        self.data_access.save_measurement(plant_id, water, temperature, humidity, light, moisture)
        dark_hours_start, dark_hours_end = self.data_access.get_dark_hours(plant_id)
        silent_hours_start, silent_hours_start = self.data_access.get_silent_hours(plant_id)
        collected_light = self.data_access.get_todays_light_exposure(plant_id)

    def configure(self, mac_address):
        return self.data_access.configure(mac_address)
