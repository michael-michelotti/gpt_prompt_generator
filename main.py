# My goal is to create a Python script which iterates over a project recursively
# and copies the text of every file into a text file with some minimal text before each
# module, explaining the module

import pathlib
import re

# General steps:
# Initialization - create write buffer, write project overview to write buffer
# Establish ignore list
with open("prompt_ignore") as fid:
    ignore_list = [entry.strip() for entry in fid.readlines()]

project_root_dir = pathlib.Path.cwd()
out_file_path = pathlib.Path(f"{project_root_dir.name}_gpt_prompt.txt")
out_buff = open(out_file_path, "w")
out_buff.write(f"My project is called {project_root_dir.name}\n")

# Start by writing entry point context to output buffer
entry_point_file = pathlib.Path(__file__)
out_buff.write(f"The entry point to my project is called {entry_point_file.name}. Here is the full text\n")
with open(entry_point_file) as fid:
    out_buff.write(fid.read())


def filter_file_list(file_iter, ignore_list):
    # Find all files at root level, remove with filter criteria
    file_list = []
    for file in project_root_dir.iterdir():
        for ignore_string in ignore_list:
            if re.search(ignore_string, file.name):
                continue
        # Filter out files or directories that should be ignored
        if file.name == entry_point_file.name or file.name == out_file_path.name:
            continue

        file_list.append(file)

    return file_list


file_list = filter_file_list(project_root_dir.iterdir(), ignore_list)

# Begin iteration over all files and directories
for file in file_list:
    # If the file is a directory, enter directory and begin recursively iterating
    if file.is_dir():
        out_buff.write(f"My project has a directory called {file.name}.\n")
        for f2 in file.iterdir():
            out_buff.write(f"That directory has a file called {file.name} with the following text:\n")
            with open(f2) as f2id:
                out_buff.write(f2id.read())
        continue

    # Write file context to write buffer
    out_buff.write(f"My project has a file called {file.name} with the following text:\n")
    with open(file) as fid:
        out_buff.write(fid.read())

# Write intermediate buffer to final buffer
# Right now, only buffer is the output file

# Cleanup (write closing context, close file)
out_buff.write("Try to convince me that this script could be improved, and provide examples.\n")
out_buff.close()
