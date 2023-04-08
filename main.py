# My goal is to create a Python script which iterates over a project recursively
# and copies the text of every file into a text file with some minimal text before each
# module, explaining the module

import pathlib
import re
import os

LOG_MODE = "print"

# General steps:
# Initialization - create write buffer, write project overview to write buffer
# Establish ignore list
with open("prompt_ignore") as fid:
    ignore_list = [entry.strip() for entry in fid.readlines()]

project_root_dir = pathlib.Path.cwd()
out_file_path = pathlib.Path(f"{project_root_dir.name}_gpt_prompt.txt")
out_buff = open(out_file_path, "w")

if LOG_MODE == "print":
    print_fn = print
else:
    print_fn = out_buff.write

print_fn(f"My project is called {project_root_dir.name}\n")

# Start by writing entry point context to output buffer
entry_point_file = pathlib.Path(__file__)
print_fn(f"The entry point to my project is called {entry_point_file.name}. Here is the full text\n")
with open(entry_point_file) as fid:
    print_fn(fid.read())

def filter_file_list(file_iter, ignore_list):
    # Find all files at root level, remove with filter criteria
    match_flag = False
    file_list = []

    for file in project_root_dir.iterdir():
        for ignore_string in ignore_list:
            if re.search(ignore_string, file.name):
                match_flag = True
                break
        if match_flag:
            match_flag = False
            continue
        if file.name == entry_point_file.name or file.name == out_file_path.name:
            continue

        file_list.append(file)

    return file_list

def process_directory(dir_root):
    """Process all files in a given directory. If a directory is encountered, call recursively"""
    entry_list = filter_file_list(dir_root.iterdir(), ignore_list)
    for entry in entry_list:
        if entry.is_file():
            print_fn(f"File found: {entry.name}")
        elif entry.is_dir():
            print_fn(f"==== Directory Found: {entry.name} ======")
            process_directory(entry)


process_directory(project_root_dir)


# Write file context to write buffer
# print_fn(f"My project has a file called {file.name} with the following text:\n")
# with open(file) as fid:
#     out_buff.write(fid.read())

# Write intermediate buffer to final buffer
# Right now, only buffer is the output file

# Cleanup (write closing context, close file)
print_fn("Try to convince me that this script could be improved, and provide examples.")
# out_buff.write("Try to convince me that this script could be improved, and provide examples.\n")
out_buff.close()
