import sys


class SimpleInterpreter:

    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.readlines()
        self.variables = {}
        self.in_multiline_comment = False

    def interpret(self):
        for line in self.lines:
            self.process_line(line.strip())

    def process_line(self, line):
        if line.startswith("#"):
            return
        if not line:
            return
        if "/*" in line:
            self.in_multiline_comment = True
        if "*/" in line:
            self.in_multiline_comment = False
            return
        if self.in_multiline_comment:
            return
        if line.startswith("print"):
            self.process_print(line)
        elif "=" in line:
            var_name, value = line.split("=")
            var_name = var_name.strip()
            value = value.strip()
            if any((op in value for op in "+-*/")):
                self.variables[var_name] = eval(value, self.variables)
            elif value.isdigit():
                self.variables[var_name] = int(value)
            elif value.startswith('"') and value.endswith('"'):
                self.variables[var_name] = value[1:-1]
            elif value in self.variables:
                self.variables[var_name] = self.variables[value]
            else:
                print("Invalid syntax in line: " + line)
                sys.exit(1)
        else:
            print("Invalid syntax in line: " + line)
            sys.exit(1)

    def process_print(self, line):
        line = line[6:-1].strip()
        if line.startswith('"') and line.endswith('"'):
            print(line[1:-1])
        elif line in self.variables:
            print(self.variables[line])
        elif any((op in line for op in "+-*/")):
            print(eval(line, self.variables))
        else:
            print("Invalid syntax")
            sys.exit(1)


def main():
    interpreter = SimpleInterpreter("code.txt")
    interpreter.interpret()


if __name__ == "__main__":
    main()
