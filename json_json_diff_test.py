#!/usr/bin/env python
import sys
import os
import unittest

class TestHelper(unittest.TestCase):

    def make_tmp_directory(self):
        if not os.path.exists('tmp/'):
            os.mkdir('tmp/')

    def write_string_to_file(self, string, filename):
        self.make_tmp_directory()
        f = open('tmp/' + str(filename), 'w')
        f.write(str(string))
        f.close()
        return 'tmp/' + str(filename)

    def write_files_to_directory(self, filename_to_string, sub_directory):
        self.make_tmp_directory()
        for filename, string in iteritems(filename_to_string):
            if not os.path.exists('tmp/' + sub_directory):
                os.mkdir('tmp/' + sub_directory)
            f = open('tmp/' + sub_directory + '/' + filename, 'w')
            f.write(str(string))
            f.close()
        return 'tmp/' + sub_directory

    def cleanup(self):
        self.cleanup_directory('tmp')

    def cleanup_directory(self, path):
        if not os.path.isdir(path):
            return
        for filename in os.listdir(path):
            if not os.path.isdir(path+'/'+filename):
                os.remove(path+'/'+filename)
            else:
                self.cleanup_directory(path+'/'+filename)
                os.rmdir(path+'/'+filename)

from six import iteritems
from json_regex_diff.jsondiff import JsonDiff

class JsonJsonDiffTest(TestHelper):

    def test_simple_no_difference(self):
        """
        With no difference we should have an empty list
        """
        new_file = self.write_string_to_file('["test"]', "item1")
        old_file = self.write_string_to_file('["test"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False), [])
        self.cleanup()

    def test_simple_type_difference(self):
        """
        When the type changes we should get an appropriate message
        in the difference
        :return:
        """
        new_file = self.write_string_to_file('["test"]', "item1")
        old_file = self.write_string_to_file('{"key":"value"}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        if sys.version_info.major == 3:
            self.assertEqual(comparison_tool.diff(use_model=False),
                             ["TypeDifference :  - is list: (['test']), "
                              "but was dict: ({'key': 'value'})"])
        else:
            self.assertEqual(comparison_tool.diff(use_model=False),
                             ["TypeDifference :  - is list: ([u'test']), "
                              "but was dict: ({u'key': u'value'})"])
        self.cleanup()

    def test_list_addition_to_end(self):
        """
        When we add an item to the front of a list we should get an
        appropriate string in the diff telling us what was added
        """
        new_file = self.write_string_to_file('["test1", "test2"]', "item1")
        old_file = self.write_string_to_file('["test1"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [1]=test2'])
        self.cleanup()

    def test_list_addition_to_front(self):
        """
        When we add an item to the end of a list we should get an
        appropriate string in the diff telling us what was added
        """
        new_file = self.write_string_to_file('["test2", "test1"]', "item1")
        old_file = self.write_string_to_file('["test1"]', "item0")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [0]=test2'])
        self.cleanup()

    def test_list_subtraction_from_front(self):
        """
        When we add an item to the end of a list we should get an
        appropriate string in the diff telling us what was added
        """
        new_file = self.write_string_to_file('["test2"]', "item1")
        old_file = self.write_string_to_file('["test1", "test2"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'-: [0]=test1'])
        self.cleanup()

    def test_list_subtraction_from_end(self):
        """
        When we add an item to the end of a list we should get an
        appropriate string in the diff telling us what was added
        """
        new_file = self.write_string_to_file('["test2"]', "item1")
        old_file = self.write_string_to_file('["test2", "test1"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'-: [1]=test1'])
        self.cleanup()

    def test_switch_order(self):
        new_file = self.write_string_to_file('["test1", "test2"]', "item1")
        old_file = self.write_string_to_file('["test2", "test1"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [1]=test2', u'-: [0]=test2'])
        self.cleanup()

    def test_list_subtract_multiple_matches(self):
        """
        When multiple list items match, we should pick the first one.
        """
        new_file = self.write_string_to_file('["test1"]', "item1")
        old_file = self.write_string_to_file('["test1", "test1"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'-: [1]=test1'])
        self.cleanup()

    def test_list_subtract_more_multiple_matches(self):
        """
        When multiple list items match, we should pick the first one.
        This test ensures that the indices of additional duplicate matches
        are correct.
        """
        new_file = self.write_string_to_file('["test1"]', "item1")
        old_file = self.write_string_to_file('["test1", "test1", "test1"]',
                                             "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'-: [2]=test1', u'-: [1]=test1'])
        self.cleanup()

    def test_list_add_multiple_matches(self):
        """
        When multiple list items match, we should pick the first one.
        """
        new_file = self.write_string_to_file('["test1", "test1"]', "item1")
        old_file = self.write_string_to_file('["test1"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [1]=test1'])
        self.cleanup()

    def test_list_add_more_multiple_matches(self):
        """
        When multiple list items match, we should pick the first one.
        This test ensures that the indices of additional duplicate matches
        are correct.
        """
        new_file = self.write_string_to_file('["test1", "test1", "test1"]',
                                             "item1")
        old_file = self.write_string_to_file('["test1"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [1]=test1', u'+: [2]=test1'])
        self.cleanup()

    def test_simple_value_difference(self):
        """
        Due to the nature of lists, we have to note specific insertions and
        deletions as opposed to listing 'Changes'
        :return:
        """
        new_file = self.write_string_to_file('["test"]', "item1")
        old_file = self.write_string_to_file('["other"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [0]=test', u'-: [0]=other'])
        self.cleanup()

    def test_completely_different_lists_difference(self):
        """
        Due to the nature of lists, we have to note specific insertions and
        deletions as opposed to listing 'Changes'
        :return:
        """
        new_file = self.write_string_to_file(
            '["test1", "test2", "test3"]', "item1")
        old_file = self.write_string_to_file(
            '["other1", "other2", "other3"]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [0]=test1', u'+: [1]=test2', u'+: [2]=test3',
                         u'-: [0]=other1', u'-: [1]=other2', u'-: [2]=other3'])
        self.cleanup()

    def test_simple_map_value_difference(self):
        """
        For maps we should be able to tell that a specific value changed if the
        keys match
        :return:
        """
        new_file = self.write_string_to_file('{"key":"value1"}', "item1")
        old_file = self.write_string_to_file('{"key":"value2"}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        if sys.version_info.major == 3:
            self.assertEqual(comparison_tool.diff(use_model=False),
                             [u"Changed: key to b'value1' from b'value2'"])
        else:
            self.assertEqual(comparison_tool.diff(use_model=False),
                             [u'Changed: key to value1 from value2'])
        self.cleanup()

    def test_simple_map_key_difference(self):
        """
        If a key changes, we must treat the maps as completely different
        objects even if their values change
        :return:
        """
        new_file = self.write_string_to_file('{"key1":"value1"}', "item1")
        old_file = self.write_string_to_file('{"key2":"value1"}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: key1=value1', u'-: key2=value1'])
        self.cleanup()

    def test_duplicate_value(self):
        """
        Since the keys are different we should match on the first key, and then
        treat the different key with the same value as a whole new object
        """
        new_file = self.write_string_to_file('{"key1":"value1", '
                                             '"key2":"value1"}', "item1")
        old_file = self.write_string_to_file('{"key1":"value1"}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: key2=value1'])
        self.cleanup()

    def test_equal_maps_nested_in_list(self):
        new_file = self.write_string_to_file('[{"key1":"value1"}]', "item1")
        old_file = self.write_string_to_file('[{"key1":"value1"}]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False), [])
        self.cleanup()

    def test_delete_from_nested_maps_in_list(self):
        new_file = self.write_string_to_file('[{"key2":"value2"}]', "item1")
        old_file = self.write_string_to_file('[{"key1":"value1", '
                                             '"key2":"value2"}]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'-: [0].key1=value1'])
        self.cleanup()

    def test_add_to_nested_map_in_list(self):
        new_file = self.write_string_to_file('[{"key1":"value1", '
                                             '"key2":"value2"}]', "item2")
        old_file = self.write_string_to_file('[{"key2":"value2"}]', "item1")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: [0].key1=value1'])
        self.cleanup()

    def test_equal_list_nested_in_map(self):
        new_file = self.write_string_to_file('{"key1":["value1"]}', "item1")
        old_file = self.write_string_to_file('{"key1":["value1"]}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False), [])
        self.cleanup()

    def test_unequal_list_nested_in_map(self):
        new_file = self.write_string_to_file('{"key1":["value2"]}', "item1")
        old_file = self.write_string_to_file('{"key1":["value1"]}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: key1[0]=value2', u'-: key1[0]=value1'])
        self.cleanup()

    def test_add_to_list_nested_in_map(self):
        new_file = self.write_string_to_file('{"key1":["value1", "value2"]}',
                                             "item1")
        old_file = self.write_string_to_file('{"key1":["value1"]}', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'+: key1[1]=value2'])
        self.cleanup()

    def test_subtract_from_list_nested_in_map(self):
        new_file = self.write_string_to_file('{"key1":["value2"]}', "item1")
        old_file = self.write_string_to_file('{"key1":["value1","value2"]}',
                                             "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        self.assertEqual(comparison_tool.diff(use_model=False),
                         [u'-: key1[0]=value1'])
        self.cleanup()

    def test_similar_nested_maps_in_list(self):
        """
        We have a known issue where out of order nested maps will find a match
        for the first item in the new list if there is anything that can match
        at all, even if there is a better match elsewhere
        """
        # todo fix this bug in matching

        new_file = self.write_string_to_file('[{"key1":"value1"},'
                                             '{"key1":"value1",'
                                             '"key2":"value2"}]', "item1")
        old_file = self.write_string_to_file('[{"key1":"value1",'
                                             '"key2":"value2"}]', "item2")
        comparison_tool = JsonDiff.from_file(new_file, old_file)
        if sys.version_info.major == 3:
            self.assertEqual(
                sorted(comparison_tool.diff(use_model=False)),
                sorted([
                    "-: [0].key2=value2",
                    "+: [1].key2=b'value2'",
                    "+: [1].key1=b'value1'"
                ]))
        else:
            self.assertEqual(comparison_tool.diff(use_model=False), [
                u'-: [0].key2=value2',
                u'+: [1].key2=value2',
                u'+: [1].key1=value1'
            ])
        # Ideally should return: +: [0].key1=value1
        self.cleanup()
if __name__ == '__main__':
    unittest.main()