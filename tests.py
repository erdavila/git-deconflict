import unittest

from deconflict import ConflictMarker, State


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
