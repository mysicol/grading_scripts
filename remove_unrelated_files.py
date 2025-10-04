from argparse import ArgumentParser
import os
from zipfile import ZipFile

parser = ArgumentParser(description="Utility to unpack code into directories for grading.")
parser.add_argument("gradebook", type=str, help="the gradebook zipfile")
args = parser.parse_args()

# make a gradebook directory
target_directory = os.path.join(os.path.dirname(args.gradebook), "gradebook")

# get my assignments
my_assignments = []
with open(os.path.join(os.path.dirname(args.gradebook), "gradinglist.csv"), "r") as file:
    for line in file:
        line = line.split(",")
        if line[0] == "ABBY":
            my_assignments.append(line[3])
        
if not os.path.exists(target_directory):
    os.mkdir(target_directory)

# extract gradebook zip
with ZipFile(args.gradebook, "r") as gradebook_zip:
    gradebook_zip.extractall(path=target_directory)

for filename in os.listdir(target_directory):
    # tokenize filename
    file_tokens = filename.split("_")
    if len(file_tokens) < 2:
        continue

    # get student ID
    student_id = file_tokens[1]
    student_directory = os.path.join(target_directory, student_id)

    if student_id not in my_assignments:
        # remove zip file
        os.remove(os.path.join(target_directory, filename))