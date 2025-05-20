from agents.script_agent import generate_psadt_script

def run_script_generation(installer_filename: str) -> str:
    return generate_psadt_script(installer_filename)