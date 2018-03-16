from peewee import *
from datetime import datetime

db = MySQLDatabase('AdvancedAgriculture', user='root', passwd='admin', host='localhost')


class Plants(Model):
    Id = PrimaryKeyField()
    MACAddress = FixedCharField(12)
    Name = CharField(null=True)
    SoilMoistureLowTreshold = IntegerField(null=True)
    SoilMoistureHighTreshold = IntegerField(null=True)
    TemperatureLowTreshold = FloatField(null=True)
    TemperatureHighTreshold = FloatField(null=True)
    HumidityLowTreshold = IntegerField(null=True)
    HumidityHighTreshold = IntegerField(null=True)
    LightLowTreshold = IntegerField(null=True)
    LightHighTreshold = IntegerField(null=True)

    class Meta:
        database = db


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


class Settings(Model):
    PlantId = ForeignKeyField(Plants, field='Id', on_delete='Cascade', on_update='Cascade')
    DarkHoursStart = TimeField()
    DarkHoursEnd = TimeField()
    SilentHoursStart = TimeField()
    SilentHoursEnd = TimeField()

    class Meta:
        database = db
        primary_key = CompositeKey('PlantId')


db.connect()


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

    def configure(self, mac_address: str):
        plant, created = Plants.get_or_create(MACAddress=mac_address)
        return plant.Id

    def get_todays_light_exposure(self, plant_id: int):
        query = Measurements.select().where((Measurements.PlantId == plant_id)
                                            & (Measurements.MeasureTime > datetime.now()
                                               .replace(hour=0, minute=0, second=0, microsecond=0)))
        collected_light = []
        for measurement in query:
            collected_light.append(measurement.Light)
        return collected_light

    def get_dark_hours(self, plant_id: int) -> Tuple[datetime, datetime]:
        pass

    def get_silent_hours(self, plant_id: int) -> Tuple[datetime, datetime]:
        pass
