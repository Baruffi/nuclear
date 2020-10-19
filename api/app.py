from flask import Flask
from redis import Redis
from model.sensors import PowerSensor, PressureSensor, FlowSensor, TemperatureSensor

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

gep = PowerSensor('GEP', 450, 8.722)                #power
sg1fwp = PressureSensor('SG1FWP', 5.2, 0.03793)     #presure1
sg2fwp = PressureSensor('SG2FWP', 5.2, 0.04199)     #presure2
sg1fwf = FlowSensor('SG1FWF', 90, 25.34)            #flow1
sg2fwf = FlowSensor('SG2FWF', 120, 33.63)           #flow2
sg1sp = PressureSensor('SG1SP', 6.4, 0.02893)       #presure3
sg2sp = PressureSensor('SG2SP', 6.4, 0.02927)       #presure4
sg1sf = FlowSensor('SG1SF', 100, 35.04)             #flow3
sg2sf = FlowSensor('SG2SF', 140, 44.91)             #flow4
dtl1 = TemperatureSensor('DTL1', 177, 0.6807)       #temperature1
dtl2 = TemperatureSensor('DTL2', 93, 0.6615)        #temperature2


@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

#power
@app.route('/power', defaults={'external': 0.0})
@app.route('/power/<float:external>')
def power(external):
    return gep.read(external)


#temperature
@app.route('/temperature1', defaults={'external': 0.0})
@app.route('/temperature1/<float:external>')
def temperature(external):
    return dtl1.read(external)

@app.route('/temperature2', defaults={'external': 0.0})
@app.route('/temperature2/<float:external>')
def temperature2(external):
    return dtl2.read(external * 1.1)


#pressure
@app.route('/pressure1', defaults={'external': 0.0})
@app.route('/pressure1/<float:external>')
def pressure(external):
    return sg1fwp.read(external)

@app.route('/pressure2', defaults={'external': 0.0})
@app.route('/pressure2/<float:external>')
def pressure2(external):
    return sg2fwp.read(external * 1.1)

@app.route('/pressure3', defaults={'external': 0.0})
@app.route('/pressure3/<float:external>')
def pressure3(external):
    return sg1sp.read(external * 1.2)

@app.route('/pressure4', defaults={'external': 0.0})
@app.route('/pressure4/<float:external>')
def pressure4(external):
    return sg2sp.read(external * 1.32)


#flow
@app.route('/flow1', defaults={'external': 0.0})
@app.route('/flow1/<float:external>')
def flow(external):
    return sg1fwf.read(external)

@app.route('/flow2', defaults={'external': 0.0})
@app.route('/flow2/<float:external>')
def flow2(external):
    return sg2fwf.read(external * 1.1)

@app.route('/flow3', defaults={'external': 0.0})
@app.route('/flow3/<float:external>')
def flow3(external):
    return sg1sf.read(external * 1.2)

@app.route('/flow4', defaults={'external': 0.0})
@app.route('/flow4/<float:external>')
def flow4(external):
    return sg2sf.read(external * 1.32)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
