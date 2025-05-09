import os
from mcp.server.fastmcp import FastMCP
import shutil
from glob import glob


SANDBOX_FOLDER = os.path.abspath("./.sandbox")
os.makedirs(SANDBOX_FOLDER, exist_ok=True)

server = FastMCP("Filesystem")


# Secure path helper
def secure_path(path: str) -> str:
    full_path = os.path.abspath(os.path.join(SANDBOX_FOLDER, path.strip("/")))
    if not full_path.startswith(SANDBOX_FOLDER):
        raise ValueError("Access outside sandbox is forbidden.")
    return full_path


@server.tool()
async def list_files(folder: str = ".") -> list | str:
    """
    List files and folders in the given directory.
    @param folder - the folder to list files in relative path. defaults to "." current folder
    @return - list of filenames/dirnames or a string of an error message
    """
    try:
        folder_path = secure_path(folder)
        _files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                _files.append(os.path.relpath(os.path.join(root, file), SANDBOX_FOLDER))
        return _files
    except Exception as e:
        return f"Error: {e}"


@server.tool()
async def read_file(filename: str) -> str:
    """
    Read contents of a file.
    @param filename - name of a file
    @return - Contents of the file or a string starting with Error: followed by an error message
    """
    try:
        file_path = secure_path(filename)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"


@server.tool()
async def write_file(filename: str, content: str) -> str:
    """
    Write content to a file, creating it if it does not exist.
    @param filename - name of file.
    @param content - Content to write to/replace in the file
    @return - Confirmation message
    """
    try:
        file_path = secure_path(filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return "file written."
    except Exception as e:
        return f"Error: {e}"


@server.tool()
async def delete_file(filename: str) -> str:
    """
    Delete a file.
    @param filename - name of file
    @return Confirmation message
    """
    try:
        file_path = secure_path(filename)
        for item in glob(
            os.path.relpath(file_path, SANDBOX_FOLDER), root_dir=SANDBOX_FOLDER
        ):
            file = os.path.join(SANDBOX_FOLDER, item)
            if os.path.isfile(file):
                os.remove(file)
            else:
                shutil.rmtree(file)
        os.makedirs(SANDBOX_FOLDER, exist_ok=True)
        return "File deleted."
    except Exception as e:
        return f"Error: {e}"
