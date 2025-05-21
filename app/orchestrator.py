from agents.script_agent import generate_psadt_script
import logging


def run_script_generation(installer_filename: str, version, installer_type) -> str:
    logging.info(f"Calling Script Agent for: {installer_filename}")
    return generate_psadt_script(installer_filename, version, installer_type)