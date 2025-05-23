from app.agents.script_agent import generate_psadt_script
import logging


def run_script_generation(packageID: str) -> str:
    # Integrate with packageID to fetch details
    # Assuming a simple mock for now, replace with actual data retrieval
    installer_filename = (
        "mock_installer.exe"  # This should be fetched based on packageID
    )
    version = "1.0"  # Fetch from data source
    installer_type = "EXE"  # Determine based on packageID
    logging.info(f"Generating script for packageID: {packageID}")
    return generate_psadt_script(installer_filename, version, installer_type)
