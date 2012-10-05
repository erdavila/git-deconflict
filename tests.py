import unittest

from deconflict import ConflictMarker


class MarkerTest(unittest.TestCase):

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
