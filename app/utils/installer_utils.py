def get_installer_type(filename: str) -> str:
    """
    Determine the installer type based on the file extension.

    Args:
        filename (str): The name of the installer file.

    Returns:
        str: 'MSI', 'EXE', or 'UNKNOWN'
    """
    filename = filename.lower()
    if filename.endswith('.msi'):
        return 'MSI'
    elif filename.endswith('.exe'):
        return 'EXE'
    else:
        return 'UNKNOWN'


