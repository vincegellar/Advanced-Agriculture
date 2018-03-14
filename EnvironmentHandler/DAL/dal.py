from peewee import *

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

    def save_measurement(self, plant_id, water, temperature, humidity, light, moisture):
        measurement = Measurements()
        measurement.PlantId = plant_id
        measurement.WaterLevel = water
        measurement.Temperature = temperature
        measurement.Humidity = humidity
        measurement.Light = light
        measurement.SoilMoisture = moisture
        measurement.save(force_insert=True)

    def get_id_by_address(self, mac_address):
        pass

    def configure(self, mac_address):
        pass

    def get_todays_light_exposure(self, plant_id):
        pass
