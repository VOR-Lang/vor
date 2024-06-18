import sys
import importlib
import argparse


class SimpleInterpreter:

    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.readlines()
        self.variables = {}
        self.functions = {}
        self.in_multiline_comment = False
        self.in_function_definition = False
        self.current_function = None

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
        if line.startswith("endfunc"):
            self.in_function_definition = False
            self.current_function = None
        elif line.startswith("define"):
            self.process_function(line)
        elif line.startswith("module"):
            self.process_module(line)
        elif self.in_function_definition:
            self.functions[self.current_function]["lines"].append(line)
        elif "::" in line:
            self.process_concatenation(line)
        elif "=" in line and "input" in line:
            self.process_input(line)
        elif line.startswith("print"):
            self.process_print(line)
        elif "(" in line and ")" in line:
            self.call_function(line)
        elif "=" in line:
            var_name, value = line.split("=")
            var_name = var_name.strip()
            value = value.strip()
            if any((op in value for op in "+-*/")):
                try:
                    self.variables[var_name] = eval(value, self.variables)
                except TypeError:
                    print(
                        f"Invalid operation in line: {line}. Check the types of the operands."
                    )
                    sys.exit(1)
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

    def process_function(self, line):
        func_name, args = (
            line.split("define ")[1].split("(")[0],
            line.split("(")[1].split(")")[0],
        )
        self.functions[func_name] = {
            "args": [arg.strip() for arg in args.split(",")],
            "lines": [],
        }
        self.in_function_definition = True
        self.current_function = func_name

    def call_function(self, func_name):
        args = []
        if "(" in func_name and ")" in func_name:
            func_name, args = (
                func_name.split("(")[0],
                func_name.split("(")[1].split(")")[0],
            )
            if args:
                args = [eval(arg.strip(), self.variables) for arg in args.split(",")]
        if "." in func_name:
            module_name, function_name = func_name.split(".")
            if module_name in self.variables and hasattr(
                self.variables[module_name], function_name
            ):
                function = getattr(self.variables[module_name], function_name)
                function(*args)
            else:
                print(f"Function {func_name} is not defined.")
                sys.exit(1)
        elif func_name in self.functions:
            func_args = self.functions[func_name]["args"]
            if len(args) < len(func_args):
                args += [None] * (len(func_args) - len(args))
            for arg, value in zip(func_args, args):
                self.variables[arg] = value
            for line in self.functions[func_name]["lines"]:
                self.process_line(line)
        else:
            print(f"Function {func_name} is not defined.")
            sys.exit(1)

    def process_module(self, line):
        parts = line.split(" ")
        if len(parts) == 2:
            module_name = parts[1]
            if module_name == "system":
                from vorlang import system

                self.variables["system"] = system
            try:
                self.variables[module_name] = importlib.import_module(module_name)
            except ImportError:
                print(f"Module {module_name} could not be imported.")
                sys.exit(1)
        else:
            print("Invalid module statement")
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
            print("Invalid syntax in line: " + line)
            sys.exit(1)

    def process_input(self, line):
        var_name, rest = line.split("=", 1)
        var_name = var_name.strip()
        if rest.strip().startswith("input"):
            prompt = rest.split("(", 1)[1].rstrip(")").strip('"')
            self.variables[var_name] = input(prompt)

    def process_concatenation(self, line):
        var_name, rest = line.split("=", 1)
        var_name = var_name.strip()
        parts = rest.strip().split("::")
        result = ""
        for part in parts:
            part = part.strip()
            if part in self.variables:
                result += self.variables[part]
            elif part.startswith('"') and part.endswith('"'):
                result += part[1:-1]
            else:
                print(f"Invalid syntax in line: {line}")
                sys.exit(1)
        self.variables[var_name] = result


def main():
    parser = argparse.ArgumentParser(
        description="Interpreter for the VOR programming language."
    )
    parser.add_argument("filename", help="The name of the file to interpret.")
    args = parser.parse_args()
    if not args.filename.endswith(".vor"):
        print("Invalid file extension. Only .vor files are supported.")
        sys.exit(1)
    interpreter = SimpleInterpreter(args.filename)
    interpreter.interpret()


if __name__ == "__main__":
    main()
