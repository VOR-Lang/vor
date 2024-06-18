import subprocess

subprocess.run("python3 setup.py sdist", shell=True)
subprocess.run("twine upload dist/*", shell=True)
subprocess.run("rm -rf dist", shell=True)
subprocess.run("rm -rf vorlang.egg-info", shell=True)