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

    @time_cycle('power_cycle', [[1.0, 4], [1.05, 3], [1.1, 2], [1.15, 1], [1.2, 1], [1.25, 20]])
    def read(self, external: float, power_cycle: float):
        value = round(normalvariate(self.mean, self.variance)
                      * power_cycle + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 'MW'
        }


class PressureSensor(Sensor):

    @time_cycle('pressure_cycle', [[1.25, 1], [1.2, 2], [1.15, 4], [1.1, 4], [1.05, 2], [1.0, 1]])
    def read(self, external: float, pressure_cycle: float):
        value = round(normalvariate(self.mean, self.variance)
                      * pressure_cycle + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 'MPa'
        }


class FlowSensor(Sensor):

    @time_cycle('flow_cycle', [[1.25, 1], [1.2, 2], [1.15, 4], [1.1, 4], [1.05, 2], [1.0, 1]])
    def read(self, external: float, flow_cycle: float):
        value = round(normalvariate(self.mean, self.variance)
                      * flow_cycle + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 't/h'
        }


class TemperatureSensor(Sensor):

    @time_cycle('temperature_cycle', [[1.0, 5], [1.05, 4], [1.1, 3], [1.15, 1], [1.1, 3], [1.05, 4]])
    def read(self, external: float, temperature_cycle: float):
        value = round(normalvariate(self.mean, self.variance)
                      * temperature_cycle + external, 5)

        super_read = super().read(external)

        return {
            **super_read,
            'value': str(value),
            'unit': 'Celcius'
        }
