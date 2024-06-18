import ast
import black
import os
import subprocess


def remove_comments_and_format(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())
    code_without_comments = ast.unparse(tree)
    formatted_code = black.format_str(code_without_comments, mode=black.FileMode())
    with open(file_path, "w") as source:
        source.write(formatted_code)


def remove_pycache():
    try:
        subprocess.run(["rm", "-rf", "__pycache__"])
    except FileNotFoundError:
        pass


python_files = [f for f in os.listdir("./") if f.endswith(".py")]
for file in python_files:
    remove_comments_and_format(f"./{file}")
remove_pycache()
