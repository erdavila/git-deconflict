#!/bin/env python


def main():
    pass


class ConflictMarker(object):
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.name)

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
    

ConflictMarker.BEGIN = ConflictMarker('BEGIN')
ConflictMarker.ANCESTOR = ConflictMarker('ANCESTOR')
ConflictMarker.DELIMITER = ConflictMarker('DELIMITER')
ConflictMarker.END = ConflictMarker('END')


if __name__ == "__main__":
    main()
