from functions.getfilesinfo import getfilesinfo
from functions.getfilecontent import getfilecontent
from functions.runpythonfile import runpythonfile
from functions.writefile import writefile
from google.genai import types

def callfunction(functioncallpart,verbose=False):
    
    workingdir = "calculator"

    if verbose == True:
        print(f"Calling function: {functioncallpart.name}({functioncallpart.args})")

    else:
        print(f"Calling function:{functioncallpart.name}")

    if functioncallpart.name == "getfilesinfo":
        result = getfilesinfo(workingdir,**functioncallpart.args)

    if functioncallpart.name == "getfilecontent":
        result = getfilecontent(workingdir,**functioncallpart.args)

    if functioncallpart.name == "runpythonfile":
        result = runpythonfile(workingdir,**functioncallpart.args)

    if functioncallpart.name == "writefile":
        result = writefile(workingdir,**functioncallpart.args)

    if result=="":
        return types.Content(
            role = "tool",
            parts = [
                types.Part.from_function_response(
                    name = functioncallpart.name,
                response = {"error": f"Unknown function: {functioncallpart.name}"},
                ),
            ]
        )
    
    return types.Content(
        role = "tool",
        parts = [
            types.Part.from_function_response(
                name = functioncallpart.name,
                response = {"result":result},
            )
        ],
    )


    