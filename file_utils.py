
import os
from werkzeug.utils import secure_filename


UPLOAD_DIRECTORY = "uploads"  


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def save_file_to_directory(file):
    """
    Saves the uploaded file to the designated upload directory.

    Args:
        file: The file object to be saved.

    Returns:
        str: The filename of the saved file (not the full path).
    
    Raises:
        Exception: If there is an error while saving the file.
    """
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        file.save(file_path)
        return filename 
    except Exception as e:
        print(f"Error saving file {file.filename}: {e}")
        raise Exception("Could not save file") from e
