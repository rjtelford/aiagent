import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the given Python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file that will be ran, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to be passed to the Python file",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_file_path = os.path.commonpath([working_dir_abs, full_file_path]) == working_dir_abs

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", full_file_path]

        if not args == None:
            command.extend(args)
        
        completed_proc = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30) 

        return_str = ""
        if not completed_proc.returncode == 0:
            return_str += f"Process exited with code {completed_proc.returncode}\n"

        if completed_proc.stdout is None and completed_proc.stderr is None: 
            return_str += f"No output produced\n"
        
        if completed_proc.stdout:
            return_str += f"STDOUT: {completed_proc.stdout}\n"
        if completed_proc.stderr:
            return_str += f"STDERR: {completed_proc.stderr}\n"

        return return_str
        
        
    except Exception as e:
        return f"Error: executing Python file: {e}"