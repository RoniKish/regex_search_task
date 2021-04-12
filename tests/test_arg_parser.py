import os
import sys
app_src_folder = os.path.abspath('./app')
sys.path.insert(0, app_src_folder)

import pytest
from main import get_parsed_args


def test_single_script_input():
    parsed_args = get_parsed_args(['regex', 'f_name'])
    compare_parsed_args(parsed_args, [False, False, False, 'regex', ['f_name']])


def test_multi_scripts_input():
    parsed_args = get_parsed_args(['regex', 'f_name_1', 'f_name_2', 'f_name_3'])
    compare_parsed_args(parsed_args, [False, False, False, 'regex', ['f_name_1', 'f_name_2', 'f_name_3']])


def test_no_file_input():
    parsed_args = get_parsed_args(['regex'])
    compare_parsed_args(parsed_args, [False, False, False, 'regex', '-'])


def test_no_input():
    with pytest.raises(SystemExit):
        get_parsed_args([])


@pytest.mark.parametrize("test_input, expected",
                         [(['True', 'False', 'False'], [True, False, False]),
                          (['False', 'True', 'False'], [False, True, False]),
                           (['False', 'False', 'True'], [False, False, True])])
def test_parse_optional_param(test_input, expected):
    parsed_args = get_parsed_args(['regex', 'f_name', '-c', test_input[0], '-u', test_input[1], '-m', test_input[2]])
    compare_parsed_args(parsed_args, [expected[0], expected[1], expected[2], 'regex', ['f_name']])


def test_2_optional_param():
    with pytest.raises(ValueError):
        get_parsed_args(['regex', 'f_name', '-c', 'True', '-u', 'True'])


def compare_parsed_args(parsed_args, expected_args):
    assert parsed_args.add_color == expected_args[0]
    assert parsed_args.add_underscore == expected_args[1]
    assert parsed_args.gen_machine_output == expected_args[2]
    assert parsed_args.regex_pattern == expected_args[3]
    for parsed_f_name, expected_f_name in zip(parsed_args.input_files, expected_args[4]):
        assert parsed_f_name == expected_f_name


