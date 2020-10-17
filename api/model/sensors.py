import random


class Sensor(object):
    def __init__(self, mean=0):
        self.mean = mean

    def read(self, external=0):
        return str(self.mean + external)


class TemperatureSensor(Sensor):
    def __init__(self, mean=0, variance=0):
        super().__init__(mean)
        self.variance = variance

    def read(self, external=0):
        return str(round(random.gauss(self.mean, self.variance) + external, 1)) + " C"
