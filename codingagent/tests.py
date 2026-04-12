from functions.getfilesinfo import getfilesinfo
from functions.getfilecontent import getfilecontent
from functions.writefile import writefile
from functions.runpythonfile import runpythonfile

def main():
    workingdir = "calculator"
    print(runpythonfile(workingdir,"main.py", ["3 + 5"]))
    




main() 