from peewee import *
from datetime import datetime, time
import configparser
from os import path

config = configparser.RawConfigParser()
config.read(path.join(path.dirname(__file__), '../EnvironmentHandler.cfg'))
user_name = config.get('Database', 'user')
password = config.get('Database', 'password')

db = MySQLDatabase('AdvancedAgriculture', user=user_name, passwd=password, host='localhost')


class Plants(Model):
    Id = PrimaryKeyField()
    MACAddress = FixedCharField(12)
    Name = CharField()
    SoilMoistureLowTreshold = IntegerField()
    SoilMoistureHighTreshold = IntegerField()
    TemperatureLowTreshold = FloatField()
    TemperatureHighTreshold = FloatField()
    HumidityLowTreshold = IntegerField()
    HumidityHighTreshold = IntegerField()
    LightLowTreshold = IntegerField()
    LightHighTreshold = IntegerField()
    PotSize = IntegerField(default=30)

    class Meta:
        database = db
        table_name = "Plants"


class Measurements(Model):
    MeasureTime = DateTimeField()
    Plant = ForeignKeyField(Plants, field='Id', on_delete='Cascade', on_update='Cascade', column_name='PlantId')
    SoilMoisture = IntegerField()
    Temperature = FloatField()
    Humidity = IntegerField()
    Light = IntegerField()
    WaterLevel = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('MeasureTime', 'Plant')
        table_name = "Measurements"


class Settings(Model):
    Plant = ForeignKeyField(Plants, field='Id', on_delete='Cascade', on_update='Cascade', column_name='PlantId')
    DarkHoursStart = TimeField()
    DarkHoursEnd = TimeField()
    SilentHoursStart = TimeField()
    SilentHoursEnd = TimeField()

    class Meta:
        database = db
        primary_key = CompositeKey('Plant')
        table_name = "Settings"


db.connect()


class PlantData:
    def __init__(self, plant: Plants, settings: Settings=None):
        self.moisture_low = plant.SoilMoistureLowTreshold
        self.moisture_high = plant.SoilMoistureHighTreshold
        self.temp_low = plant.TemperatureLowTreshold
        self.temp_high = plant.TemperatureHighTreshold
        self.humidity_low = plant.HumidityLowTreshold
        self.humidity_high = plant.HumidityHighTreshold
        self.light_low = plant.LightLowTreshold
        self.light_high = plant.LightHighTreshold
        self.pot_size = plant.PotSize
        if settings is None:
            self.dark_hours_start = time().replace(hour=0, minute=0, second=0, microsecond=0)
            self.dark_hours_end = time().replace(hour=0, minute=0, second=0, microsecond=0)
            self.silent_hours_start = time().replace(hour=0, minute=0, second=0, microsecond=0)
            self.silent_hours_end = time().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            self.dark_hours_start = settings.DarkHoursStart
            self.dark_hours_end = settings.DarkHoursEnd
            self.silent_hours_start = settings.SilentHoursStart
            self.silent_hours_end = settings.SilentHoursEnd


class DataAccess:

    def save_measurement(self, plant_id: int, water: int, temperature: float, humidity: int, light: int, moisture: int):
        measurement = Measurements()
        measurement.MeasureTime = datetime.now()
        measurement.Plant = plant_id
        measurement.WaterLevel = water
        measurement.Temperature = temperature
        measurement.Humidity = humidity
        measurement.Light = light
        measurement.SoilMoisture = moisture
        measurement.save(force_insert=True)

    def configure(self, mac_address: str) -> int:
        plant, created = Plants.get_or_create(MACAddress=mac_address, Name='', SoilMoistureLowTreshold=0,
                                              SoilMoistureHighTreshold=0, TemperatureLowTreshold=0.0,
                                              TemperatureHighTreshold=0.0, HumidityLowTreshold=0,
                                              HumidityHighTreshold=0, LightLowTreshold=0, LightHighTreshold=0)
        return plant.Id

    def get_todays_light_exposure(self, plant_id: int) -> list:
        query = Measurements.select().where((Measurements.Plant == plant_id)
                                            & (Measurements.MeasureTime > datetime.now()
                                               .replace(hour=0, minute=0, second=0, microsecond=0)))
        collected_light = []
        for measurement in query:
            collected_light.append(measurement.Light)
        return collected_light

    def get_plant_data(self, plant_id: int) -> PlantData:
        plant = Plants.select().where(Plants.Id == plant_id)
        plant_settings = Settings.select().where(Settings.Plant == plant_id)
        if not plant.exists():
            raise ValueError('No plant found.')
        if not plant_settings.exists():
            return PlantData(plant[0])
        return PlantData(plant[0], plant_settings[0])
