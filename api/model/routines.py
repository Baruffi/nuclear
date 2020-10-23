class Routine(object):

    def __init__(self, id: str, stages: dict[str, list[float]] = {}):
        self.id = id
        self.stages = stages

    def get_id(self):
        return self.id

    def add_stage(self, stage_name: str, stage_values: list[int]):
        self.stages[stage_name] = stage_values

    def get_stage(self, stage_name: str):
        return self.stages[stage_name]
