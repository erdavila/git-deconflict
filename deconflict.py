#!/bin/env python
import os.path


def main():
    pass


class Output(object):
    
    def __init__(self, name, file_designator):
        self.name = name
        self.file_designator = file_designator
    
    def make_filename(self, filename):
        base, ext = os.path.splitext(filename)
        return base + '.' + self.file_designator + ext

Output.ANCESTOR = Output('ANCESTOR', '1')
Output.OURS = Output('OURS', '2')
Output.THEIRS = Output('THEIRS', '3')

Output.ALL = (Output.ANCESTOR, Output.OURS, Output.THEIRS)


class State(object):
    
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
    
    def __repr__(self):
        return self.__class__.__name__ + '.' + self.name

State.COMMON = State('COMMON', (Output.ANCESTOR, Output.OURS, Output.THEIRS,))
State.OURS = State('OURS', (Output.OURS,))
State.ANCESTOR = State('ANCESTOR', (Output.ANCESTOR,))
State.THEIRS = State('THEIRS', (Output.THEIRS,))


class ConflictMarker(object):
    
    def __init__(self, name, triggered_state):
        self.name = name
        self.triggered_state = triggered_state
    
    def __repr__(self):
        return self.__class__.__name__ + '.' + self.name

    @classmethod
    def identify(cls, line):
        if line.startswith('<<<<<<<'):
            return ConflictMarker.BEGIN
        elif line.startswith('|||||||'):
            return ConflictMarker.ANCESTOR
        elif line.startswith('======='):
            return ConflictMarker.DELIMITER
        elif line.startswith('>>>>>>>'):
            return ConflictMarker.END
        else:
            return None

ConflictMarker.BEGIN = ConflictMarker('BEGIN', State.OURS)
ConflictMarker.ANCESTOR = ConflictMarker('ANCESTOR', State.ANCESTOR)
ConflictMarker.DELIMITER = ConflictMarker('DELIMITER', State.THEIRS)
ConflictMarker.END = ConflictMarker('END', State.COMMON)


if __name__ == "__main__":
    main()
