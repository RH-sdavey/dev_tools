import re


class ConsoleParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_output(console):
        print(f"---HERE---{console}\n")

    @staticmethod
    def find_build(console):
        return int(re.search(r"#\d{4}", console).group().strip('#'))
