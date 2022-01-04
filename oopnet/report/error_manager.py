from re import compile

from oopnet.report.simulation_errors import get_error_list, EPANETSimulationError


class ErrorManager:
    def __init__(self):
        self.found_errors = []
        self._error_exp = compile(r'\d{3}: ')
        self._error_list = get_error_list()

    def check_line(self, text_line) -> bool:
        text_line = text_line.replace('\n', '')
        matches = self._error_exp.search(text_line)
        if matches:
            raised_code = matches.group()
            raised_code_int = int(matches.group().replace(': ', ''))
            error_text = text_line.split(raised_code)[1]
            for error in self._error_list:
                if raised_code_int == error.code:
                    self.found_errors.append([error, error_text, None])
                    return True
        return False

    def append_error_message(self, text_line):
        text_line = text_line.replace('\n', '').strip()
        err = self.found_errors[-1]
        err[2] = text_line

    def raise_errors(self):
        if self.found_errors:
            raise EPANETSimulationError([err(msg, details) for err, msg, details in self.found_errors])
