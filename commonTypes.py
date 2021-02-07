from typing import NewType, Dict

LevelString = NewType('LevelString', bytes)
RobDict = NewType('RobDict', Dict[str, str])


class RobtopEnumError(Exception):
    def __init__(self, enum: int):
        self.enum = enum
        self.message = str(enum)

        super().__init__(self.message)
