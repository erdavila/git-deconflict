#!/bin/env python
import os.path


def main():
    pass


def make_ancestor_filename(filename):
    return make_output_filename(filename, '1')

def make_ours_filename(filename):
    return make_output_filename(filename, '2')

def make_theirs_filename(filename):
    return make_output_filename(filename, '3')

def make_output_filename(filename, num):
    base, ext = os.path.splitext(filename)
    return base + '.' + num + ext
    


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
