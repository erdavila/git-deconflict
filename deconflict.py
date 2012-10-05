#!/bin/env python


def main():
    pass


class FileKey(object):
    
    ANCESTOR = 'ANCESTOR'
    OURS = 'OURS'
    THEIRS = 'THEIRS'


class State(object):
    
    def __init__(self, name, file_keys):
        self.name = name
        self.file_keys = file_keys
    
    def __repr__(self):
        return self.__class__.__name__ + '.' + self.name

State.COMMON = State('COMMON', (FileKey.ANCESTOR, FileKey.OURS, FileKey.THEIRS,))
State.OURS = State('OURS', (FileKey.OURS,))
State.ANCESTOR = State('ANCESTOR', (FileKey.ANCESTOR,))
State.THEIRS = State('THEIRS', (FileKey.THEIRS,))


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
