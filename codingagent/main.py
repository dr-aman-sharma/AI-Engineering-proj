import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.getfilesinfo import schemagetfilesinfo
from functions.getfilecontent import schemagetfilecontent
from functions.runpythonfile import schemarunpythonfile
from functions.writefile import schemawritefile
from callfunction import callfunction


def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    systemprompt = ("""  
    You are a helpful coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations: 
    -list files and directories
    -Read the content of a file 
    -Write a file (create or update)
    -Run a python file with optional arguments.

    When the user asks about code project, they are referring to the working directory.
    So, you should typically start by looking at project's files,
    and figuring out how to run project and how to run its tests, you will
    always want to test the tests and the actual project to verify that the 
    behaviour is working.

    All paths you provide should be relative to working directory. You do not need to specify the working directory in your function calls as it is automatically injected
    for security reasons.
    """)

    if len(sys.argv)<2:
        print("I need prompt")
        sys.exit(1)
    
    prompt= sys.argv[1] 
    
    verboseflag = False

    if len(sys.argv) == 3 and sys.argv[2] == "verbose":
        verboseflag = True

    messages = [
        types.Content(role="user", parts = [types.Part(text=prompt)]),
    ]

    availfuncts = types.Tool(
    function_declarations=[schemagetfilesinfo,
                           schemagetfilecontent,
                           schemarunpythonfile,
                           schemawritefile
                           ],
    )

    config = types.GenerateContentConfig(
        tools=[availfuncts], system_instruction = systemprompt
    )


    maxiters=20
    for i in range(maxiters):
        response = client.models.generate_content(model = "gemini-2.5-flash",
                                                contents=messages, 
                                                config = config,
                                                )


        if response is None or response.usage_metadata is None:
            print("usage is empty:")
            return
        
        if verboseflag == True:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)

        
        if response.function_calls:
            for functioncallpart in response.function_calls:
                result = callfunction(functioncallpart,verboseflag)
                messages.append(result)
                

        else:
            print(response.text)
            return
    


   


    



main()