from peewee import *
from datetime import datetime, time

db = MySQLDatabase('AdvancedAgriculture', user='root', passwd='admin', host='localhost')


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
    PlantId = ForeignKeyField(Plants, field='Id', on_delete='Cascade', on_update='Cascade')
    SoilMoisture = IntegerField()
    Temperature = FloatField()
    Humidity = IntegerField()
    Light = IntegerField()
    WaterLevel = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('MeasureTime', 'PlantId')
        table_name = "Measurements"


class Settings(Model):
    PlantId = ForeignKeyField(Plants, field='Id', on_delete='Cascade', on_update='Cascade')
    DarkHoursStart = TimeField()
    DarkHoursEnd = TimeField()
    SilentHoursStart = TimeField()
    SilentHoursEnd = TimeField()

    class Meta:
        database = db
        primary_key = CompositeKey('PlantId')
        table_name = "Settings"


db.connect()


class PlantData:
    def __init__(self, moisture_low: int, moisture_high: int, temp_low: float, temp_high: float, humidity_low: int,
                 humidity_high: int, light_low: int, light_high: int, dark_hours_start: time, dark_hours_end: time,
                 silent_hours_start: time, silent_hours_end: time, pot_size: int):
        self.moisture_low = moisture_low
        self.moisture_high = moisture_high
        self.temp_low = temp_low
        self.temp_high = temp_high
        self.humidity_low = humidity_low
        self.humidity_high = humidity_high
        self.light_low = light_low
        self.light_high = light_high
        self.dark_hours_start = dark_hours_start
        self.dark_hours_end = dark_hours_end
        self.silent_hours_start = silent_hours_start
        self.silent_hours_end = silent_hours_end
        self.pot_size = pot_size


class DataAccess:

    def save_measurement(self, plant_id: int, water: int, temperature: float, humidity: int, light: int, moisture: int):
        measurement = Measurements()
        measurement.PlantId = plant_id
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
        query = Measurements.select().where((Measurements.PlantId == plant_id)
                                            & (Measurements.MeasureTime > datetime.now()
                                               .replace(hour=0, minute=0, second=0, microsecond=0)))
        collected_light =[]
        for measurement in query:
            collected_light.append(measurement.Light)
        return collected_light

    def get_plant_data(self, plant_id: int) -> PlantData:
        plant = Plants.select().where(Plants.Id == plant_id)
        plant_settings = Settings.select().where(Settings.PlantId == plant_id)
        if not plant.exists():
            raise ValueError('No plant found.')
        if not plant_settings.exist():
            return PlantData(plant.MoistureLowTreshold, plant.MoistureHighTreshold, plant.TemperatureLowTreshold,
                             plant.TemperatureHighTreshold, plant.HumidityLowTreshold, plant.HumidityHighTreshold,
                             plant.LightLowTreshold, plant.LightHighTreshold,
                             time().replace(hour=0, minute=0, second=0, microsecond=0),
                             time().replace(hour=0, minute=0, second=0, microsecond=0),
                             time().replace(hour=0, minute=0, second=0, microsecond=0),
                             time().replace(hour=0, minute=0, second=0, microsecond=0), plant.PotSize)
        return PlantData(plant.MoistureLowTreshold, plant.MoistureHighTreshold, plant.TemperatureLowTreshold,
                         plant.TemperatureHighTreshold, plant.HumidityLowTreshold, plant.HumidityHighTreshold,
                         plant.LightLowTreshold, plant.LightHighTreshold, plant_settings.DarkHoursStart,
                         plant_settings.DarkHoursEnd, plant_settings.SilentHoursStart, plant_settings.SilentHoursEnd,
                         plant.PotSize)
