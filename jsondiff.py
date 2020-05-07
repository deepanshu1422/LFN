#!/usr/bin/env python
import argparse
import copy
import json
import logging
import os
import re

from builtins import bytes
from six import text_type


class JsonDiff(object):
    def __init__(self, new_json, model_map, logger=logging.getLogger(),
                 is_directory=False, list_depth=0):

        self._logger = logger
        self.new_json = new_json

        self.model = model_map
        self.is_directory = is_directory

        self.difference = []
        # variable to control how deep to recursively search
        
        self.list_depth = list_depth

    @classmethod
    def from_json(cls, new_json, old_json, logger=logging.getLogger()):
       
        model_map = {'old_json': old_json}
        return cls(new_json, model_map, logger, is_directory=False)

    @classmethod
    def from_file(cls, json_file, json_model, logger=logging.getLogger()):
        

        try:
            new_json = json.load(open(json_file))
        except IOError:
            logger.error("JSON File not found. ")
            new_json = None
            exit(1)

        # Set up model map
        model_map = {}
        if os.path.isfile(json_model):
            is_directory = False
            try:
                model_map[json_model] = json.load(open(json_model))
            except IOError:
                logger.error("Model file not found. "
                             )
                exit(1)
        elif os.path.isdir(json_model):
            is_directory = True
            for item in os.listdir(json_model):
                try:
                    if not json_model.endswith('/'):
                        json_model += '/'
                    filename = json_model + item
                    model_map[item] = json.load(open(filename))
                except IOError:
                    logger.error("Could not open file")
        else:
            is_directory = False
            logger.error("File or directory not found. "
                         "Check name and try again.")
            exit(1)

        if len(model_map) < 1:
            logger.error("No file to read ")
            exit(1)

        return cls(new_json, model_map, logger, is_directory)

    @staticmethod
    def _clear_match_row(match_table, row, cur_index):
        for i in range(len(match_table[0])):
            match_table[row][i] = 0
        match_table[row][cur_index] = 1

    @staticmethod
    def _clear_match_col(match_table, col, cur_index):
        for i in range(len(match_table[0])):
            match_table[i][col] = 0
        match_table[cur_index][col] = 1

    def _one_to_one(self, strings, regexes):
        dim = len(strings)
        match_chart = [[0 for i in range(dim)] for j in range(dim)]

        
        for r in range(dim):
            for s in range(dim):
                match = re.match(regexes[r], strings[s])
                if match:
                    match_chart[r][s] = 1

        
        sums = [sum(match_chart[k][:]) for k in range(dim)]
        # add in columns
        sums.extend(sum([match_chart[i][j] for i in range(dim)])
                    for j in range(dim))

        num_matches, index, turns_wo_match = 0, 0, 0
        max_index = 2 * dim
        minimized = [False for i in range(2 * dim)]
        # loop until all matched or no more minimization is possible
        while num_matches < max_index and turns_wo_match < max_index \
                and not sums == [1] * (2 * dim):
            if sums[index] == 0:
                return {}  # no match for one of the fields
            elif sums[index] == 1 and not minimized[index]:
                # find coordinate
                if index < dim:  # in a row
                    for i in range(dim):
                        if match_chart[index][i] == 1:
                            self._clear_match_col(match_chart, i, index)
                            minimized[index] = True
                            continue
                else:  # in a col
                    for i in range(dim):
                        if match_chart[i][index] == 1:
                            self._clear_match_row(match_chart, i, index)
                            minimized[index] = True
                            continue
                turns_wo_match = 0
                num_matches += 1
                # update sums
                sums = [sum(match_chart[k][:]) for k in range(dim)]
                # add in columns
                sums.extend(sum([match_chart[i][j] for i in range(dim)])
                            for j in range(dim))

            else:
                turns_wo_match += 1

            index = (index + 1) % max_index

        if num_matches == max_index or sums == [1] * (2 * dim):
            final_mapping = {}
            for i in range(dim):
                # find match
                for j in range(dim):
                    if match_chart[i][j] == 1:
                        final_mapping[regexes[i]] = strings[j]
                        continue
            return final_mapping

        else:  # ambiguous
            self._logger.error("Ambiguous matching please fix your model "
                               )
            exit(1)

    def _lists_equal(self, json_list, regex_list):
       
        if not len(json_list) == len(regex_list):
            return False

        
        for index in range(len(json_list)):
            if not type(json_list[index]) == type(regex_list[index]):
                return False

            if isinstance(json_list[index], dict):
               
                if not self.equals_model(json_list[index], regex_list[index]):
                    return False

            elif isinstance(json_list[index], list):
               
                if not self._lists_equal(json_list[index], regex_list[index]):
                    return False

            elif isinstance(json_list[index], text_type):
                # regex match
                if not re.match(regex_list[index], json_list[index]):
                    return False

            else:
               
                if not json_list[index] == regex_list[index]:
                    return False

        return True

    def equals_model(self, json_input, model):
        
        json_keys = []
        model_keys = []
        if isinstance(json_input, dict) and isinstance(model, dict):
            json_keys = list(json_input)
            model_keys = list(model)
        elif isinstance(json_input, list) and isinstance(model, list):
            return self._lists_equal(json_input, model)
        elif type(json_input) is not type(model):
            return False
        else:
            self._logger.error("Not proper JSON format. "
                               )
            exit(1)

        
        if not len(json_keys) == len(model_keys):
            return False

        # check 1-1 correspondence
        key_matches = self._one_to_one(json_keys, model_keys)

        if not len(json_keys) == len(list(key_matches)):
            return False

        
        for key in key_matches:
            if not type(json_input.get((key_matches[key]))) == \
                    type(model[key]):
                return False
            if isinstance(model[key], dict):
                # recursive search
                if not self.equals_model(json_input.get(key_matches[key]),
                                         model[key]):
                    return False
                    #  continue

            elif isinstance(model[key], list):
                # lists are good
                if not self._lists_equal(json_input.get(key_matches[key]),
                                         model[key]):
                    return False

            elif isinstance(model[key], text_type):
                if not re.match(model[key], json_input.get(key_matches[key])):
                    return False

            
            else:
                if not json_input.get(key_matches[key]) == model[key]:
                    return False

        # if we make it through all of this Yes!!!
        return True

    @staticmethod
    def equals_json(_json1, _json2):
        
        return _json1 == _json2

    def diff_model(self, _json1, _json2, path='', depth=-1):
        if not type(_json1) == type(_json2):
            if isinstance(
                    _json2, text_type) and type(_json1) not in [list, dict]:
                # Potential regex match
                self._diff_json_item(_json1, _json2, path, True)
            else:
                self.difference.append('TypeDifference : {} - {}:'
                                       ' ({}), {}: ({})'
                                       .format(path, type(_json1).__name__,
                                               text_type(_json1),
                                               type(_json2).__name__,
                                               text_type(_json2)))
        else:
            # they are the same type
            
            if isinstance(_json1, dict):
                self._diff_json_dict(_json1, _json2, path, depth, True)
            elif isinstance(_json1, list):
                self._diff_json_list(_json1, _json2, path, depth, True)
            else:
                self._diff_json_item(_json1, _json2, path, True)

    def diff_json(self, _json1, _json2, path='', depth=-1):
       
        if not type(_json1) == type(_json2):
            self.difference.append('TypeDifference : {} - is {}: ({}),'
                                   ' but was {}: ({})'
                                   .format(path, type(_json1).__name__,
                                           text_type(_json1),
                                           type(_json2).__name__,
                                           text_type(_json2)))
        else:
            
            if isinstance(_json1, dict):
                self._diff_json_dict(_json1, _json2, path, depth, False)
            elif isinstance(_json1, list):
                self._diff_json_list(_json1, _json2, path, depth, False)
            else:
                self._diff_json_item(_json1, _json2, path, False)

    def _diff_json_dict(self, _json1, _json2, path, depth, use_regex):
        
        if not depth == 0:
            json1_keys = list(_json1)
            json2_keys = list(_json2)
            matched_keys = []
            for key in json1_keys:
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = '{}.{}'.format(path, key)
                if key in json2_keys:
                    # match
                    matched_keys.append(key)
                    json2_keys.remove(key)
                else:
                  
                    self._expand_diff(_json1[key], new_path, True)
            for key in json2_keys:
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = '{}.{}'.format(path, key)
                
                self._expand_diff(_json2[key], new_path, False)

            # now that we have matched keys, recursively search
            for key in matched_keys:
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = '{}.{}'.format(path, key)
                if use_regex:
                    self.diff_model(_json1[key], _json2[key], new_path,
                                    depth - 1)
                else:
                    self.diff_json(_json1[key], _json2[key], new_path,
                                   depth - 1)

    def _diff_json_list(self, _json1, _json2, path, depth, use_regex):
        
        current_difference = copy.deepcopy(self.difference)
        json2_original = copy.deepcopy(_json2)
        json1_matches = []
       
        cur_index = 0
        for (index, item) in enumerate(_json1):
            prev_index = cur_index
           
            index_to_irrelevance = {}
           
            index_to_changeset = {}
            while cur_index < len(_json2):
                if not use_regex and item == _json2[cur_index]:
                    # perfect match
                    index_to_irrelevance[cur_index] = 0
                    json1_matches.append(item)
                    _json2.remove(_json2[cur_index])
                    break
                elif use_regex and type(item) not in [list, dict]:
                    if isinstance(_json2[cur_index], text_type):
                       
                        match = re.match(_json2[cur_index], text_type(item))
                        if match:
                            index_to_irrelevance[cur_index] = 0
                            json1_matches.append(item)
                            _json2.remove(_json2[cur_index])
                            break
                        else:
                            # no possible match
                            index_to_irrelevance[cur_index] = -1
                    else:
                        # Can't use regex-- test strict equality
                        if item == _json2[cur_index]:
                            # perfect match
                            index_to_irrelevance = 0
                            json1_matches.append(item)
                            _json2.remove(_json2[cur_index])
                        else:
                           
                            index_to_irrelevance[cur_index] = -1
                            continue
                elif depth == 0 or type(item) not in [list, dict] or type(
                        item) is not type(_json2[cur_index]):
                    # failed surface match
                   
                    index_to_irrelevance[
                        cur_index] = -1  # to indicate no possible match
                else:
                    
                    new_path = "{}[{}]".format(path, index)
                    if use_regex:
                        self.diff_model(item, _json2[cur_index], new_path,
                                        depth - 1)
                    else:
                        self.diff_json(item, _json2[cur_index], new_path,
                                       depth - 1)
                    
                    index_to_irrelevance[cur_index] = len(
                        [diff_item for diff_item in self.difference if
                         diff_item not in current_difference])
                    index_to_changeset[cur_index] = [diff_item for diff_item in
                                                     self.difference if
                                                     diff_item not in
                                                     current_difference]
                    # set difference back to before the diff
                    self.difference = copy.deepcopy(current_difference)
                    self._logger.debug("Resetting diff from recursive branch")
                cur_index += 1

            
            indices = list(index_to_irrelevance)
            if len(indices) == 0:
                break
            indices.sort()
            best_match_score = -1
            match_index = indices[0]
            for i in indices:
                if index_to_irrelevance[i] == 0:
                    best_match_score = 0
                    break
                elif index_to_irrelevance[i] < 0:
                    continue
                else:
                    if best_match_score < 0 \
                            or index_to_irrelevance[i] < best_match_score:
                        best_match_score = index_to_irrelevance[i]
                        match_index = i
            if best_match_score > 0:
               
                self.difference.extend(index_to_changeset[match_index])
                for entry in index_to_changeset[match_index]:
                    self._logger.debug(entry)
                json1_matches.append(item)
                _json2.remove(_json2[match_index])
                cur_index = match_index  # Should be the after the match
            elif best_match_score < 0:
                cur_index = prev_index

        
        match_index = 0
        for index in range(len(_json1)):
            if match_index < len(json1_matches) and _json1[index] == \
                    json1_matches[match_index]:
                match_index += 1
            else:
                new_path = "{}[{}]".format(path, index)
                self._expand_diff(_json1[index], new_path, True)

        original_index = 0
        for index in range(len(_json2)):
            # Find the item in the original
            while not _json2[index] == json2_original[::-1][original_index]:
                original_index = (original_index + 1) % len(json2_original)
            new_path = "{}[{}]".format(path, len(
                json2_original) - original_index - 1)
            self._expand_diff(_json2[index], new_path, False)
            original_index = (original_index + 1) % len(json2_original)

    def _diff_json_item(self, _json1, _json2, path, use_regex):
        if isinstance(_json1, text_type) :
            _json1 = _json1.encode('ascii', 'ignore')
        if isinstance(_json2, text_type):
            _json2 = _json2.encode('ascii', 'ignore')
        if use_regex and isinstance(_json2, bytes):
            match = re.match(_json2, bytes(_json1))
            if not match:
                self.difference.append(
                    'Changed: {} to {} from {}'.format(path, _json1, _json2))
                self._logger.debug('Changed: {} to {} from {}'
                                   .format(path, _json1, _json2))
        else:
            if not _json1 == _json2:
                self.difference.append(
                    'Changed: {} to {} from {}'.format(path, _json1, _json2))
                self._logger.debug('Changed: {} to {} from {}'
                                   .format(path, _json1, _json2))

    def _expand_diff(self, blob, path, new_item):
       
        # Three possibilities: dict, list, item
        if new_item:
            c = '+'
        else:
            c = '-'
        if isinstance(blob, dict):
            for key in blob:
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = "{}.{}".format(path, key)
                if type(blob[key]) not in [list, dict]:
                    if isinstance(blob[key], text_type):
                        self.difference.append(
                            '{}: {}={}'.format(c, new_path,
                                               blob[key].encode('ascii',
                                                                'ignore')))
                        self._logger.debug('{}: {}={}'
                                           .format(c, new_path,
                                                   blob[key]
                                                   .encode('ascii', 'ignore')))
                    else:
                        self.difference.append(
                            '{}: {}={}'.format(c, new_path, blob[key]))
                        self._logger.debug(
                            '{}: {}={}'.format(c, new_path, blob[key]))
                else:
                    self._expand_diff(blob[key], new_path, new_item)
        elif isinstance(blob, list):
            for (index, item) in enumerate(blob):
                new_path = "{}[{}]".format(path, index)
                if isinstance(blob[index], (list, dict)):
                    self._expand_diff(item[index], new_path, new_item)
                    if isinstance(blob[index], text_type):
                        self.difference.append(
                            '{}: {}={}'.format(c, new_path,
                                               blob[index].encode('ascii',
                                                                  'ignore')))
                        self._logger.debug(
                            '{}: {}={}'.format(c, new_path,
                                               blob[index].encode('ascii',
                                                                  'ignore')))
                    else:
                        self.difference.append(
                            '{}: {}={}'.format(c, new_path, blob[index]))
                        self._logger.debug(
                            '{}: {}={}'.format(c, new_path, blob[index]))

                else:
                    pass
        else:
            self.difference.append('{}: {}={}'.format(c, path, blob))
            self._logger.debug('{}: {}={}'.format(c, path, blob))

    def comparison(self, use_model):
        for model_name in self.model:
            if use_model:
                if self.equals_model(self.new_json, self.model[model_name]):
                    return model_name if self.is_directory else True
            else:
                if self.equals_json(self.new_json, self.model[model_name]):
                    return model_name if self.is_directory else True
        # no match
        return False

    def diff(self, use_model):
        difference = []
        self._logger.info(self.model)
        for model_name in self.model:
            if use_model:
                self.diff_model(self.new_json, self.model[model_name])
            else:
                self.diff_json(self.new_json, self.model[model_name])
            self._logger.info('Diff from {}\n'.format(model_name))
            for change in self.difference:
                # log instead of print,
                
                self._logger.info(change.encode('ascii', 'ignore'))
            difference.append(self.difference)
            # Reinitialize so that we can run against multiple models
            self.difference = []
            self.list_depth = 0

        return difference if len(difference) > 1 else difference[0]


def main():
    p = argparse.ArgumentParser(
        description='Tool to check equivalence and difference of two JSON '
                    'files with regex support',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=
               'To do JSON to JSON comparison (default behavior):\n'
               '   ./json_diff.py path/to/file1.json path/to/file2.json \n'
               '\n'
               
               'To compute the diff between to JSON documents: \n'
               '    ./json_diff.py -d path/to/new.json path/to/old.json'

    )
    p.add_argument('--use_model', action="store_true",
                   help="Wether the file is regular or with regex support")
    p.add_argument('-d', '--diff', action="store_true",
                   help="Compute diffrence")
    p.add_argument('--logging_level', default='INFO', help="Warnings /errors")
    p.add_argument('json', help='The path of the json file')
    p.add_argument('json_model', metavar='json/json_model',
                   help="The path of the .json file or directory of .json "
                        "models with regex support"
                        
                        )

    options = p.parse_args()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger('jsondiff')
    logger.addHandler(console_handler)
    logger.setLevel(options.logging_level)

    diff_engine = JsonDiff.from_file(options.json, options.json_model, logger)

    if options.diff:
        if os.path.isdir(options.json_model):
            raise Exception(
                "Unsupported operation: "
                "Must provide a filename")
        else:
            diff_engine.diff(options.use_model)
    else:
        logger.info(diff_engine.comparison(options.use_model))


if __name__ == "__main__":
    main()

