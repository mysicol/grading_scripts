from argparse import ArgumentParser
import os

parser = ArgumentParser(description="For Windows user (me): change makefile mkdir instructions with a -p to Windows-format if not exist.")
parser.add_argument("gradebook", type=str, help="gradebook directory", default=".")
args = parser.parse_args()

# make a gradebook directory
target_directory = os.path.join(os.path.dirname(args.gradebook), "gradebook")

# parse all subdirectories to find makefiles
for root, subdirectory, files in os.walk(target_directory):
    # specifically find makefiles
    for filename in files:
        if filename.lower() == "makefile":
            lines = ""
            filepath = os.path.join(root, filename)

            # remove the -p flag from mkdirs
            with open(filepath, 'r') as file:
                lines = file.readlines()
                new_lines = []
                newt_lines = lines.copy()

                for line in lines:
                    if "mkdir" in line and "if not exist" not in line:
                        # remove -p flag
                        line = line.replace("-p", "")

                        # get the name of the directory we are making
                        split_line = line.split()
                        directory_making = ""
                        for i, word in enumerate(split_line):
                            if "mkdir" in word:
                                directory_making = split_line[i+1]
                            
                        # add an if not exist qualifier to mkdir
                        line = line.replace("mkdir", "if not exist " + directory_making + " mkdir")

                    new_lines.append(line)
            
            # overwrite file with replaced lines
            with open(filepath, 'w') as file:
                file.writelines(new_lines)
