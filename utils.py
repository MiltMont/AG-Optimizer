import os

def verify_source_file(filename):
    """Verify that the source file exists and is accessible."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Source file '{filename}' not found!")
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"'{filename}' is not a regular file!")
    if not os.access(filename, os.R_OK):
        raise FileNotFoundError(f"Source file '{filename}' is not readable!")
    
    # Check if it's a C source file
    if not filename.endswith(('.c', '.cpp')):
        raise FileNotFoundError(f"File '{filename}' does not appear to be a C/C++ source file!")
