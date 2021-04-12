import re
import pytest

from RegexSearcher import RegexSearcher, RegexSearcherUnderscore, RegexSearcherMachine, RegexSearcherColor
from main import get_parsed_args, get_regex_search_class


@pytest.mark.parametrize("test_class", [RegexSearcher, RegexSearcherUnderscore, RegexSearcherColor, RegexSearcherMachine])
def test_wrong_regex_error(test_class):
    with pytest.raises(re.error):
        test_class("[0-9]++", "--..2312")


@pytest.mark.parametrize("test_input, expected_type",
                         [(['-c', 'True'], RegexSearcherColor), (['-u', 'True'], RegexSearcherUnderscore),
                          (['-m', 'True'], RegexSearcherMachine), (['-c', 'False'], RegexSearcher)])
def test_get_regex_searcher_classes(test_input, expected_type):
    args = get_parsed_args(['regex', 'f_name', test_input[0], test_input[1]])
    regex_search_class = get_regex_search_class(args)
    assert isinstance(regex_search_class, expected_type)

