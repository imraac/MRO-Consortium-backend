
import os
from werkzeug.utils import secure_filename

# Define the directory where you want to save the uploaded files
UPLOAD_DIRECTORY = "uploads"  # Change this to your desired upload directory

# Ensure the upload directory exists
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
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        # Define the full path for saving the file
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        # Save the file
        file.save(file_path)
        return filename  # Return only the filename
    except Exception as e:
        print(f"Error saving file {file.filename}: {e}")
        raise Exception("Could not save file") from e
