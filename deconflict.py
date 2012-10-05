#!/usr/bin/env python
from __future__ import print_function
import os.path
import sys


def main():
    input_filename = sys.argv[1]
    Main(input_filename).run()
    

class Main(object):
    
    def __init__(self, input_filename):
        self.input_filename = input_filename

    def run(self):
        self.open_output_files()
        self.show_output_file_names()
        self.process_lines_from_input_file()
        self.close_output_files()

    def open_output_files(self):
        self.output_files = {}
        for output in Output.ALL:
            output_filename = output.make_filename(self.input_filename)
            output_file = open(output_filename, 'w')
            self.output_files[output] = output_file
    
    def show_output_file_names(self):
        print('Writing the following files:')
        for output in Output.ALL:
            print('\t', self.output_files[output].name)
    
    def process_lines_from_input_file(self):
        with open(self.input_filename) as input_file:
            self.state = State.COMMON
            self.process_lines(input_file)

    def process_lines(self, input_file):
        for line in input_file:
            self.process_line(line)

    def process_line(self, line):
        marker = ConflictMarker.identify(line)
        if marker is None:
            self.write_line_to_outputs(line)
        else:
            self.state = marker.triggered_state

    def write_line_to_outputs(self, line):
        for output in self.state.outputs:
            output = self.output_files[output]
            output.write(line)

    def close_output_files(self):
        for output in self.output_files.itervalues():
            output.close()



class Output(object):
    
    def __init__(self, name, file_designator):
        self.name = name
        self.file_designator = file_designator
    
    def make_filename(self, filename):
        base, ext = os.path.splitext(filename)
        return base + '.' + self.file_designator + ext

Output.ANCESTOR = Output('ANCESTOR', 'ancestor')
Output.OURS = Output('OURS', 'ours')
Output.THEIRS = Output('THEIRS', 'theirs')

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
