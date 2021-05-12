import argparse
import re
import sys

from RegexSearcher import RegexSearcher, RegexSearcherColor, RegexSearcherUnderscore, RegexSearcherMachine


def get_parsed_args(args):
    parser = argparse.ArgumentParser()
    add_positional_args_to_parser(parser)
    add_optional_args_to_parser(parser)
    parsed_args = parser.parse_args(args)
    if list(parsed_args.__dict__.values()).count(True) > 1:
        raise ValueError("Optional parameters are mutually exclusive, more then 1 True value was found")
    return parsed_args


def add_positional_args_to_parser(parser):
    parser.add_argument('regex_pattern', type=validate_arg_regex_type,
                        help='regular expression pattern to search for')
    parser.add_argument('input_files', nargs='*',
                        help='files path to search the regular expression inside', default="-")


def add_optional_args_to_parser(parser):
    parser.add_argument('-u', '--underscore', action="store", dest="add_underscore", type=validate_arg_bool_type,
                        help="prints '^' under the matching text, boolean value", default=False)
    parser.add_argument('-c', '--color', action="store", dest="add_color", type=validate_arg_bool_type,
                        help="highlight matching text, boolean value", default=False)
    parser.add_argument('-m', '--machine', action="store", dest="gen_machine_output", type=validate_arg_bool_type,
                        help="generate machine readable output, boolean value", default=False)


def validate_arg_bool_type(arg):
    """Validate given arg is of bool type"""
    if isinstance(arg, bool):
        return arg
    if arg.lower() in ('true', '1', 't'):
        return True
    if arg.lower() in ('false', '0', 'f'):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected")


def validate_arg_regex_type(arg):
    """Validate given arg is a valid regex"""
    try:
        re.compile(arg)
        return arg
    except re.error:
        raise argparse.ArgumentTypeError("regular expression is not valid")


def get_std_in():
    """Get a user std in"""
    try:
        data = sys.stdin.read()
        return data.split()
    except Exception as ex:
        print("Failed to get stdin for input files: \n" + str(ex))


def get_regex_search_class(args):
    """Return a regex search class. depending on given optional parameters"""
    if args.add_color:
        return RegexSearcherColor(args.regex_pattern, args.input_files)
    if args.add_underscore:
        return RegexSearcherUnderscore(args.regex_pattern, args.input_files)
    if args.gen_machine_output:
        return RegexSearcherMachine(args.regex_pattern, args.input_files)
    else:
        return RegexSearcher(args.regex_pattern, args.input_files)


def main():
    """
    Search a regex in files
    positional parameters:
    (1) regex string
    (2) name of files to search in, separated by whitespace
    optional parameters:
    -u ( --underscore ) which prints '^' under the matching text
    -c ( --color ) which highlight matching text [1]
    -m ( --machine ) which generate machine readable output
    """
    args = get_parsed_args(sys.argv[1:])
    if args.input_files == '-' or args.input_files[0] == '-':
        print("getting data from std in\n")
        args.input_files = get_std_in()
    red_hat_regex_searcher = get_regex_search_class(args)
    red_hat_regex_searcher.search_all()
    red_hat_regex_searcher.print_all()


if __name__ == '__main__':
    main()
