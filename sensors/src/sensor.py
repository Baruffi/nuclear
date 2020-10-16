class Sensor(object):

    def sense(self, external):
        return 0


class TemperatureSensor(Sensor):

    def sense(self, external):
        return external + 1