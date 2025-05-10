from argparse import ArgumentParser
import os
from zipfile import ZipFile

parser = ArgumentParser(description="Utility to unpack code into directories for grading.")
parser.add_argument("gradebook", type=str, help="the gradebook zipfile")
args = parser.parse_args()

# make a gradebook directory
target_directory = os.path.join(os.path.dirname(args.gradebook), "gradebook")

if not os.path.exists(target_directory):
    os.mkdir(target_directory)

# extract gradebook zip
with ZipFile(args.gradebook, "r") as gradebook_zip:
    gradebook_zip.extractall(path=target_directory)

# parse list of submissions
for filename in os.listdir(target_directory):
    # tokenize filename
    file_tokens = filename.split("_")
    if len(file_tokens) < 2:
        continue

    # get student ID
    student_id = file_tokens[1]
    student_directory = os.path.join(target_directory, student_id)

    # make a directory for this student
    if not os.path.exists(student_directory):
        os.mkdir(student_directory)

    full_filename = os.path.join(target_directory, filename)

    if filename.endswith(".zip"):
        # unzip file submissions
        with ZipFile(full_filename, "r") as student_zip:
            student_zip.extractall(path=student_directory)

        # remove zip file
        os.remove(full_filename)
    elif filename.endswith(".txt"):
        # delete grade reports
        os.remove(full_filename)
    else:
        os.rename(full_filename, os.path.join(student_directory, filename))