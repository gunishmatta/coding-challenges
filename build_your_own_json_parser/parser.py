class JsonParser:
    def __init__(self,json_string):
        self.json_string = json_string
        self.current_position = 0

    def parse(self):
        return self._parse_value()

    def _parse_value(self):
        self._skip_whitespace()
        if self.current_position >= len(self.json_string):
            raise ValueError("Unexpected end of input")
        char = self.json_string[self.current_position]
        if char == '{':
            return self._parse_object()
        elif char == '[':
            return self._parse_array()
        elif char == '"':
            return self._parse_string()
        elif char in '-0123456789':
            return self._parse_number()
        elif char == 't' or char == 'f':
            return self._parse_boolean()
        elif char == 'n':
            return self._parse_null()
        else:
            raise ValueError(f"Unexpected character: {char}")

    def _parse_object(self):
        self.current_position +=1
        obj = {}
        self._skip_whitespace()
        if self.json_string[self.current_position] == '}':
            self.current_position += 1
            return obj
        while True:
            self._skip_whitespace()
            key = self._parse_string()
            self._skip_whitespace()
            self._expect_char(':')
            value = self._parse_value()
            obj[key] = value
            self._skip_whitespace()
            if self.json_string[self.current_position] == '}':
                self.current_position += 1  # Skip '}'
                break
            elif self.json_string[self.current_position] == ',':
                self.current_position += 1
            else:
                raise ValueError("Expected '}' or ',' but found: " + self.json_string[self.current_position])
        return obj


    def _parse_array(self):
        self.current_position += 1  # Skip '['
        arr = []
        self._skip_whitespace()

        if self.json_string[self.current_position] == ']':
            self.current_position += 1  # Skip ']'
            return arr
        while True:
            self._skip_whitespace()
            arr.append(self._parse_value())
            self._skip_whitespace()
            if self.json_string[self.current_position] == ']':
                self.current_position += 1
                break
            elif self.json_string[self.current_position] == ',':
                self.current_position += 1
            else:
                raise ValueError("Expected ']' or ',' but found: " + self.json_string[self.current_position])
        return arr

    def _parse_number(self):
        start_position = self.current_position
        while self.json_string[self.current_position] in '0123456789.-+eE':
            self.current_position += 1
        number_value = self.json_string[start_position:self.current_position]
        return float(number_value)

    def _parse_boolean(self):
        if self.json_string[self.current_position:self.current_position+4] == 'true':
            self.current_position += 4
            return True
        elif self.json_string[self.current_position:self.current_position+5] == 'false':
            self.current_position += 5
            return False
        else:
            raise ValueError("Unexpected boolean value")

    def _parse_null(self):
        if self.json_string[self.current_position:self.current_position+4] == 'null':
            self.current_position += 4
            return None
        else:
            raise ValueError("Unexpected null value")

    def _parse_string(self):
        self.current_position += 1
        start_pos = self.current_position
        while self.json_string[self.current_position] != '"':
            self.current_position += 1
        string_value = self.json_string[start_pos:self.current_position]
        self.current_position += 1  # Skip the closing quote
        return string_value

    def _skip_whitespace(self):
        while self.current_position < len(self.json_string) and self.json_string[self.current_position] in ' \t\n\r':
            self.current_position += 1

    def _expect_char(self, char):
        if self.json_string[self.current_position] != char:
            raise ValueError(f"Expected '{char}' but found '{self.json_string[self.current_position]}'")
        self.current_position += 1


json_string = '{"name": "Alice", "age": 25, "is_student": false, "address": null}'
parser = JsonParser(json_string)
parsed_json = parser.parse()
print(parsed_json)
