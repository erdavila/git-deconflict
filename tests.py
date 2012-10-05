import unittest

from deconflict import ConflictMarker, State, FileKey, make_ancestor_filename,\
    make_ours_filename, make_theirs_filename


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


class FileKeysByStatesTest(unittest.TestCase):
    
    def test_file_keys_in_common_state(self):
        keys = State.COMMON.file_keys
        
        self.assertEqual(len(keys), 3)
        self.assertIn(FileKey.ANCESTOR, keys)
        self.assertIn(FileKey.OURS, keys)
        self.assertIn(FileKey.THEIRS, keys)
    
    def test_file_keys_in_ours_state(self):
        keys = State.OURS.file_keys
        
        self.assertEqual(len(keys), 1)
        self.assertNotIn(FileKey.ANCESTOR, keys)
        self.assertIn(FileKey.OURS, keys)
        self.assertNotIn(FileKey.THEIRS, keys)
    
    def test_file_keys_in_ancestor_state(self):
        keys = State.ANCESTOR.file_keys
        
        self.assertEqual(len(keys), 1)
        self.assertIn(FileKey.ANCESTOR, keys)
        self.assertNotIn(FileKey.OURS, keys)
        self.assertNotIn(FileKey.THEIRS, keys)
    
    def test_file_keys_in_theirs_state(self):
        keys = State.THEIRS.file_keys
        
        self.assertEqual(len(keys), 1)
        self.assertNotIn(FileKey.ANCESTOR, keys)
        self.assertNotIn(FileKey.OURS, keys)
        self.assertIn(FileKey.THEIRS, keys)


class OutputFilenamesTests(unittest.TestCase):
    
    def test_ancestor_filename(self):
        filename = 'abc/123/xyz.ext'
        ancestor_filename = make_ancestor_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.1.ext')
    
    def test_ours_filename(self):
        filename = 'abc/123/xyz.ext'
        ancestor_filename = make_ours_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.2.ext')
    
    def test_theirs_filename(self):
        filename = 'abc/123/xyz.ext'
        ancestor_filename = make_theirs_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.3.ext')
   
    def test_ancestor_filename_without_extension(self):
        filename = 'abc/123/xyz'
        ancestor_filename = make_ancestor_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.1')
    
    def test_ours_filename_without_extension(self):
        filename = 'abc/123/xyz'
        ancestor_filename = make_ours_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.2')
    
    def test_theirs_filename_without_extension(self):
        filename = 'abc/123/xyz'
        ancestor_filename = make_theirs_filename(filename)
        self.assertEqual(ancestor_filename, 'abc/123/xyz.3')
