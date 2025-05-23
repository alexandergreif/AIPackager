import openai
from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def get_context():
    #get the context from the vector search database
    pass


def get_examples():
    #get context examples from the standard deploy-application.ps1 file for the structure
    #and also for previous versions maybe.
    pass


def ai_api_call(user_prompt, system_prompt):
    # should only call the openai Model to generate the script with the user and system prompt.

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

    response = client.responses.create(
        model="gpt-4.1",
        input=messages,
        max_output_tokens=1000,
        temperature=0.7
    )



    script = response.output_text
    return script


def generate_psadt_script(app_name, version, installer_type, user_instructions, packageID):
    # this function is used to receive all the details about the app / installer,
    # then combine it and call the ai Model over the API.
    # After that make some updates in the database and return the script.



    #system prompt has to be reqphrased for sure!!!!! maybe use the one of codex of OpenAI? something like this...
    system_prompt = (
        "You are a software packaging assistant specialized in generating PowerShell App Deployment Toolkit (PSADT) scripts for enterprise software."
        "You will be given metadata about an installer (application name, version) and should produce a valid Deploy-Application.ps1 Install section."
        "Use standard PSADT cmdlets like Show-InstallationPrompt, Execute-Process, etc. Assume the installer is silent-capable and placed in the 'Files' directory."
        "The script must be syntactically correct and safe for testing."
    )
    #user_instructions should be included in the user prompt.
    user_prompt = (
        f"Generate a PSADT Install block for the following software:\n\n"
        f"- Application: {app_name}\n"
        f"- Version: {version}\n"
        f"- Installer Type: {installer_type} (e.g., MSI or EXE)\n\n"
        "Use typical silent install switches. Place the main logic inside the "
        "Deploy-Application -DeploymentType 'Install' block."
    )




    script = ai_api_call(user_prompt, system_prompt, app_name, version)
    return script

