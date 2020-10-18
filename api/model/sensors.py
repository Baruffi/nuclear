import random


class Sensor(object):
    def __init__(self, mean=0, variance=0):
        self.mean = mean
        self.variance = variance

    def read(self, external=0):
        return str(round(random.uniform(self.mean, self.mean + self.variance) + external, 1))


class TemperatureSensor(Sensor):
    def read(self, external=0):
        return str(round(random.gauss(self.mean, self.variance) + external, 1)) + " C"
