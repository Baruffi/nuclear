from model.routine import Routine

routines = [
    Routine('power_modifier', {
            'startup': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            'running': [1],
            'shutdown': [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0],
            'stopped': [0],
            }),
    Routine('pressure_modifier', {
            'startup': [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2],
            'running': [1, 0.9, 0.8, 0.7, 0.8, 0.9],
            'shutdown': [1.2, 1, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
            'stopped': [0],
            }),
    Routine('flow_modifier', {
            'startup': [0, 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2],
            'running': [1, 0.9, 0.8, 0.7, 0.8, 0.9],
            'shutdown': [1.2, 1, 0.8, 0.6, 0.4, 0.2, 0, 0, 0, 0, 0],
            'stopped': [0],
            }),
    Routine('temperature_modifier', {
            'startup': [0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.4, 0.4, 0.6, 0.6, 0.9, 0.9, 1.2, 1.2],
            'running': [1, 1, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.8, 0.8, 0.9, 0.9],
            'shutdown': [1.2, 1.2, 0.9, 0.9, 0.6, 0.6, 0.4, 0.4, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05],
            'stopped': [0.05],
            })
]


def get_routine(id: str):
    return next((routine for routine in routines if routine.get_id() == id), None)
