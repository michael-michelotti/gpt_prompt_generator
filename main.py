# My goal is to create a Python script which iterates over a project recursively
# and copies the text of every file into a text file with some minimal text before each
# module, explaining the module

import pathlib

# General steps:
# Initialization - create write buffer, write project overview to write buffer
project_root_dir = pathlib.Path.cwd()
out_file_path = pathlib.Path(f"{project_root_dir.name}_gpt_prompt.txt")
out_buff = open(out_file_path, "w")
out_buff.write(f"My project is called {project_root_dir.name}\n")

# Start by writing entry point context to output buffer
entry_point_file = pathlib.Path(__file__)
out_buff.write(f"The entry point to my project is called {entry_point_file.name}. Here is the full text\n")
with open(entry_point_file) as fid:
    out_buff.write(fid.read())

# Begin iteration over all files and directories
for file in project_root_dir.iterdir():
    if file.name == entry_point_file.name or file.name == out_file_path.name:
        continue

    # If the file is a directory, enter directory and begin recursively iterating
    if file.is_dir():
        out_buff.write(f"My project has a directory called {file.name}.\n")
        for f2 in file.iterdir():
            out_buff.write(f"That directory has a file called {file.name} with the following text:\n")
            with open(f2) as f2id:
                out_buff.write(f2id.read())

    # Write file context to write buffer
    out_buff.write(f"My project has a file called {file.name} with the following text:\n")
    with open(file) as fid:
        out_buff.write(fid.read())

# Write intermediate buffer to final buffer
# Right now, only buffer is the output file

# Cleanup (write closing context, close file)
out_buff.write("Try to convince me that this script could be improved, and provide examples.\n")
out_buff.close()
