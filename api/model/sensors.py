from random import normalvariate
from model.cycles import time_cycle


class Sensor(object):

    def __init__(self, id: str, mean: float = 0, variance: float = 0):
        self.id = id
        self.mean = mean
        self.variance = variance

    def get_id(self):
        return self.id

    def read(self, external: float):
        return {
            'id': self.id,
            'external': str(external)
        }


class PowerSensor(Sensor):

    @time_cycle('power_modifier')
    def read(self, external: float, power_modifier: float):
        value = round(normalvariate(self.mean, self.variance)
                      * power_modifier + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 'MW'
        }


class PressureSensor(Sensor):

    @time_cycle('pressure_modifier')
    def read(self, external: float, pressure_modifier: float):
        value = round(normalvariate(self.mean, self.variance)
                      * pressure_modifier + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 'MPa'
        }


class FlowSensor(Sensor):

    @time_cycle('flow_modifier')
    def read(self, external: float, flow_modifier: float):
        value = round(normalvariate(self.mean, self.variance)
                      * flow_modifier + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 't/h'
        }


class TemperatureSensor(Sensor):

    @time_cycle('temperature_modifier')
    def read(self, external: float, temperature_modifier: float):
        value = round(normalvariate(self.mean, self.variance)
                      * temperature_modifier + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 'Celcius'
        }
