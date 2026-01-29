import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file that will be wrtten to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    try:

        working_dir_abs = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, full_file_path]) == working_dir_abs

        if not valid_file_path:
            return f'Error: Cannot wwrite to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(file_path, exist_ok=True)
        
        with open(full_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"