import random


class SensorGroup(object):
    def __init__(self, *sensors):
        self.sensors = [*sensors]

    def get_sensor(self, id):
        return next((sensor for sensor in self.sensors if sensor.id == id), None)

    def get_readings(self, **externals):
        return {'readings': [sensor.read(external) for id, external in externals.items() if (sensor := self.get_sensor(id))]}

    def get_sensors(self):
        return self.sensors

    def set_sensors(self, sensors):
        self.sensors = sensors

    def add_sensors(self, *sensors):
        self.sensors.extend(sensors)


class Sensor(object):
    def __init__(self, id='0', mean=0, variance=0):
        self.id = id
        self.mean = mean
        self.variance = variance

    def read(self):
        return {
            'id': self.id
        }


class PowerSensor(Sensor):
    def read(self, external=0):
        super_read = super().read()
        value = round(random.gauss(self.mean, self.variance) + external, 5)

        return {
            **super_read,
            'value': value,
            'unit': 'MW'
        }


class PressureSensor(Sensor):
    def read(self, external=0):
        super_read = super().read()
        value = round(random.gauss(self.mean, self.variance) + external, 5)

        return {
            **super_read,
            'value': value,
            'unit': 'MPa'
        }


class FlowSensor(Sensor):
    def read(self, external=0):
        super_read = super().read()
        value = round(random.gauss(self.mean, self.variance) + external, 5)

        return {
            **super_read,
            'value': value,
            'unit': 't/h'
        }


class TemperatureSensor(Sensor):
    def read(self, external=0):
        super_read = super().read()
        value = round(random.gauss(self.mean, self.variance) + external, 5)

        return {
            **super_read,
            'value': value,
            'unit': 'Celcius'
        }
