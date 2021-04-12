import re


class RegexSearcher:

    def __init__(self, regex_pattern, input_files):
        try:
            self.regex = re.compile(regex_pattern)
            self.input_files = input_files
            self.search_results = {}
        except re.error:
            raise re.error("regular expression is not valid")

    def search_all(self):
        for file_name in self.input_files:
            self.search_in_file(file_name)

    def search_in_file(self, file_name):
        result_lines = []
        with open(file_name) as file_to_search:
            for line_num, line in enumerate(file_to_search):
                search_results = self.regex.findall(line)
                current_line_pos = 0
                for result in search_results:
                    result_line = {"file_name": file_name,
                                   "matching_string": result,
                                   "line_string": line.rstrip(),
                                   "line_number": line_num,
                                   "match_string_pos": line.index(result, current_line_pos)}
                    result_line["final_result_line_string"] = self.get_final_result_line_string(result_line)
                    result_lines.append(result_line)
                    current_line_pos = result_line["match_string_pos"] + len(result) + 1
        self.search_results[file_name] = result_lines

    def get_final_result_line_string(self, result_line):
        return result_line['file_name'] + " > line " + str(result_line['line_number']) + \
               ": " + result_line['line_string'].rstrip()

    def get_all_search_results(self):
        return self.search_results

    def print_all(self):
        for search_result in self.search_results.values():
            for file_results in search_result:
                print(file_results['final_result_line_string'])


class RegexSearcherUnderscore(RegexSearcher):
    def get_final_result_line_string(self, result_line):
        whitespaces_num = len(result_line['file_name']) + len(" > line ") + len(str(result_line['line_number'])) + len(": ")
        whitespaces_num += result_line['match_string_pos']
        return result_line['file_name'] + " > line " + str(result_line['line_number']) + \
               ": " + result_line['line_string'].rstrip() + \
               "\r\n" + " "*whitespaces_num + "^"*len(result_line['matching_string'])


class RegexSearcherColor(RegexSearcher):
    def get_final_result_line_string(self, result_line):
        match_string_pos = result_line['match_string_pos']
        match_string_len = len(result_line['matching_string'])
        line_string = result_line['line_string']
        result_line['line_string'] = line_string[:match_string_pos] + "\033[31m" + result_line['matching_string'] + \
                                     "\033[m" + result_line['line_string'][match_string_pos + match_string_len:]
        return result_line['file_name'] + " > line " + str(result_line['line_number']) + \
               ": " + result_line['line_string'].rstrip()


class RegexSearcherMachine(RegexSearcher):
    def get_final_result_line_string(self, result_line):
        return result_line['file_name'] + ":" + str(result_line['line_number']) + \
               ":" + str(result_line['match_string_pos']) + ":" + result_line['line_string'].rstrip()
