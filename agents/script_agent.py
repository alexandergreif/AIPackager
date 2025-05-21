import openai
from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def generate_psadt_script(app_name, version, installer_type):
    system_prompt = (
        "You are a software packaging assistant specialized in generating PowerShell App Deployment Toolkit (PSADT) scripts for enterprise software."
        "You will be given metadata about an installer (application name, version) and should produce a valid Deploy-Application.ps1 Install section."
        "Use standard PSADT cmdlets like Show-InstallationPrompt, Execute-Process, etc. Assume the installer is silent-capable and placed in the 'Files' directory."
        "The script must be syntactically correct and safe for testing."
    )

    user_prompt = (
        f"Generate a PSADT Install block for the following software:\n\n"
        f"- Application: {app_name}\n"
        f"- Version: {version}\n"
        f"- Installer Type: {installer_type} (e.g., MSI or EXE)\n\n"
        "Use typical silent install switches. Place the main logic inside the "
        "Deploy-Application -DeploymentType 'Install' block."
    )

    # response = client.completions.create(
    #     model="gpt-4.1",
    #     input=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     temperature=0.7,
    #     max_tokens=1000
    # )

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