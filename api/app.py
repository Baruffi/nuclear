from flask import Flask
from redis import Redis
from model.sensors import SensorGroup, PowerSensor, PressureSensor, FlowSensor, TemperatureSensor

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

gep = PowerSensor('GEP', 450, 8.722)
sg1fwp = PressureSensor('SG1FWP', 5.2, 0.03793)
sg2fwp = PressureSensor('SG2FWP', 5.2, 0.04199)
sg1fwf = FlowSensor('SG1FWF', 90, 25.34)
sg2fwf = FlowSensor('SG2FWF', 120, 33.63)
sg1sp = PressureSensor('SG1SP', 6.4, 0.02893)
sg2sp = PressureSensor('SG2SP', 6.4, 0.02927)
sg1sf = FlowSensor('SG1SF', 100, 35.04)
sg2sf = FlowSensor('SG2SF', 140, 44.91)
dtl1 = TemperatureSensor('DTL1', 177, 0.6807)
dtl2 = TemperatureSensor('DTL2', 93, 0.6615)

power_group = SensorGroup(gep)
temperature_group = SensorGroup(dtl1, dtl2)
pressure_group = SensorGroup(sg1fwp, sg2fwp, sg1sp, sg2sp)
flow_group = SensorGroup(sg1fwf, sg2fwf, sg1sf, sg2sf)


@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')


@app.route('/power', defaults={'external': 0.0})
@app.route('/power/<float:external>')
def power(external):
    return power_group.get_readings(GEP=external)


@app.route('/temperature', defaults={'external': 0.0})
@app.route('/temperature/<float:external>')
def temperature(external):
    return temperature_group.get_readings(DTL1=external, DTL2=external * 1.1)


@app.route('/pressure', defaults={'external': 0.0})
@app.route('/pressure/<float:external>')
def pressure(external):
    return pressure_group.get_readings(SG1FWP=external, SG2FWP=external * 1.1, SG1SP=external * 1.2, SG2SP=external * 1.32)


@app.route('/flow', defaults={'external': 0.0})
@app.route('/flow/<float:external>')
def flow(external):
    return flow_group.get_readings(SG1FWF=external, SG2FWF=external * 1.1, SG1SF=external * 1.2, SG2SF=external * 1.32)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
