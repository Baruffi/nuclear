from model.sensor import Sensor, PowerSensor, PressureSensor, FlowSensor, TemperatureSensor

sensors: list[Sensor] = [
    PowerSensor('GEP', 450, 8.722),
    PressureSensor('SG1FWP', 12.22, 0.03793),
    PressureSensor('SG2FWP', 12.32, 0.04199),
    FlowSensor('SG1FWF', 29000, 25.34),
    FlowSensor('SG2FWF', 30000, 33.63),
    PressureSensor('SG1SP', 6.35, 0.02893),
    PressureSensor('SG2SP', 6.45, 0.02927),
    FlowSensor('SG1SF', 2900, 35.04),
    FlowSensor('SG2SF', 3000, 44.91),
    TemperatureSensor('DTL1', 210, 0.6807),
    TemperatureSensor('DTL2', 200, 0.6615)
]


def get_sensor(id):
    return next((sensor for sensor in sensors if sensor.get_id() == id), None)
