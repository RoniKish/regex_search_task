import os
import re
import pytest

from RegexSearcher import RegexSearcher, RegexSearcherUnderscore, RegexSearcherMachine, RegexSearcherColor
from main import get_parsed_args, get_regex_search_class


@pytest.mark.parametrize("test_class", [RegexSearcher, RegexSearcherUnderscore, RegexSearcherColor, RegexSearcherMachine])
def test_wrong_regex_error(test_class):
    with pytest.raises(re.error) as ex_info:
        test_class("[0-9]++", "--..2312")
    assert ex_info.value.message == 'regular expression is not valid'


@pytest.mark.parametrize("test_input, expected_type",
                         [(['-c', 'True'], RegexSearcherColor), (['-u', 'True'], RegexSearcherUnderscore),
                          (['-m', 'True'], RegexSearcherMachine), (['-c', 'False'], RegexSearcher)])
def test_get_regex_searcher_classes(test_input, expected_type):
    args = get_parsed_args(['regex', 'f_name', test_input[0], test_input[1]])
    regex_search_class = get_regex_search_class(args)
    assert isinstance(regex_search_class, expected_type)


@pytest.mark.parametrize("test_class", [RegexSearcher, RegexSearcherUnderscore, RegexSearcherColor, RegexSearcherMachine])
def test_search_all_function_one_file(test_class, expected_search_all_function_one_file):
    project_abs_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(project_abs_path, "./test_files/example_file_1.txt")
    my_test_class = test_class("[0][1]", [full_path])
    my_test_class.search_all()
    search_result_dict = my_test_class.search_results
    for test_file_result in search_result_dict.values():
        for result_index, search_result in enumerate(test_file_result):
            assert search_result == expected_search_all_function_one_file[test_class.__name__][result_index]
