import random

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
