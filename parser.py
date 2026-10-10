from dataclasses import dataclass

@dataclass
class ParsedInclude:
    entire_line: str
    path: str

# from cxxheaderparser.simple import parse_file, parse_string

class Parser(object):
    def _is_not_stl(self, include_path: str):
        return not include_path.startswith('<') and not include_path.endswith('>')
        # return "competitive-programming-library" in include_path and not include_path.startswith('<') and not include_path.endswith('>')

    def parse_includes(self, file_contents: str) -> list[ParsedInclude]:
        raise NotImplementedError()

class CPPParser(Parser):
    def parse_includes(self, file_contents: str) -> list[ParsedInclude]:
        sp = filter(lambda x: x.startswith("#include"), file_contents.splitlines())
        return list(filter(lambda parsed_include: self._is_not_stl(parsed_include.entire_line), map(lambda include: ParsedInclude(include, include.replace("#include", "")[2:-1]), sp)))
        # contents = parse_string(file_contents)
        # return list(filter(self._is_not_stl, map(lambda include: include.filename[1:-1], contents.includes)))
