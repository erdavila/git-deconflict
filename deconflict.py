#!/bin/env python


def main():
    pass


class State(object):
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return self.__class__.__name__ + '.' + self.name

State.COMMON = State('COMMON')
State.OURS = State('OURS')
State.ANCESTOR = State('ANCESTOR')
State.THEIRS = State('THEIRS')


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
