import unittest

from deconflict import ConflictMarker, State, Output


class MarkersTest(unittest.TestCase):

    def test_conflict_begin_marker(self):
        marker = ConflictMarker.identify('<<<<<<< HEAD')
        self.assertIs(marker, ConflictMarker.BEGIN)

    def test_conflict_ancestor_marker(self):
        marker = ConflictMarker.identify('||||||| merged common ancestors')
        self.assertIs(marker, ConflictMarker.ANCESTOR)

    def test_conflict_delimiter_marker(self):
        marker = ConflictMarker.identify('=======')
        self.assertIs(marker, ConflictMarker.DELIMITER)
    
    def test_conflict_end_marker(self):
        marker = ConflictMarker.identify('>>>>>>> them')
        self.assertIs(marker, ConflictMarker.END)
    
    def test_not_marker(self):
        marker = ConflictMarker.identify('hello')
        self.assertIs(marker, None)


class StateTriggeredByMarkersTest(unittest.TestCase):
    
    def test_conflict_begin_marker_triggers_ours_state(self):
        self.assertEqual(ConflictMarker.BEGIN.triggered_state, State.OURS);
    
    def test_conflict_ancestor_marker_triggers_ancestor_state(self):
        self.assertEqual(ConflictMarker.ANCESTOR.triggered_state, State.ANCESTOR);
    
    def test_conflict_delimiter_marker_triggers_theirs_state(self):
        self.assertEqual(ConflictMarker.DELIMITER.triggered_state, State.THEIRS);
    
    def test_conflict_end_marker_triggers_common_state(self):
        self.assertEqual(ConflictMarker.END.triggered_state, State.COMMON);


class OutputsByStatesTest(unittest.TestCase):
    
    def test_outputs_in_common_state(self):
        outputs = State.COMMON.outputs
        
        self.assertEqual(len(outputs), 3)
        self.assertIn(Output.ANCESTOR, outputs)
        self.assertIn(Output.OURS, outputs)
        self.assertIn(Output.THEIRS, outputs)
    
    def test_outputs_in_ours_state(self):
        outputs = State.OURS.outputs
        
        self.assertEqual(len(outputs), 1)
        self.assertNotIn(Output.ANCESTOR, outputs)
        self.assertIn(Output.OURS, outputs)
        self.assertNotIn(Output.THEIRS, outputs)
    
    def test_outputs_in_ancestor_state(self):
        outputs = State.ANCESTOR.outputs
        
        self.assertEqual(len(outputs), 1)
        self.assertIn(Output.ANCESTOR, outputs)
        self.assertNotIn(Output.OURS, outputs)
        self.assertNotIn(Output.THEIRS, outputs)
    
    def test_outputs_in_theirs_state(self):
        outputs = State.THEIRS.outputs
        
        self.assertEqual(len(outputs), 1)
        self.assertNotIn(Output.ANCESTOR, outputs)
        self.assertNotIn(Output.OURS, outputs)
        self.assertIn(Output.THEIRS, outputs)


class OutputFilenamesTests(unittest.TestCase):
    
    def test_ancestor_filename(self):
        filename = 'abc/123/xyz.ext'
        ancestor_filename = Output.ANCESTOR.make_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.1.ext')
    
    def test_ours_filename(self):
        filename = 'abc/123/xyz.ext'
        ancestor_filename = Output.OURS.make_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.2.ext')
    
    def test_theirs_filename(self):
        filename = 'abc/123/xyz.ext'
        ancestor_filename = Output.THEIRS.make_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.3.ext')
   
    def test_ancestor_filename_without_extension(self):
        filename = 'abc/123/xyz'
        ancestor_filename = Output.ANCESTOR.make_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.1')
    
    def test_ours_filename_without_extension(self):
        filename = 'abc/123/xyz'
        ancestor_filename = Output.OURS.make_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.2')
    
    def test_theirs_filename_without_extension(self):
        filename = 'abc/123/xyz'
        ancestor_filename = Output.THEIRS.make_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.3')
