from argparse import ArgumentParser
import os
import pathlib
import re

parser = ArgumentParser(description="Grading sequence generation assignment. There should be a directory called \"known\" in the directory this script is located in. Store known sequence files in there.")
parser.add_argument("target", type=str, help="Student directory filepath.")
args = parser.parse_args()

# Checker script filepath
known_directory = pathlib.Path(__file__).resolve().parent / "known"

lengths = []

for correct_filename in os.listdir(known_directory):
    number = re.findall(r'\d+', correct_filename)

    if len(correct_filename) > 4 and correct_filename[-4:] == ".txt" and len(number) > 0:
        lengths.append([int(number[0]), correct_filename])

lengths.sort()

for target_number, correct_filename in lengths:
    print("Checking sequences length", target_number)
    found = False
    
    for root, subdirectory, files in os.walk(args.target):
        for wrong_filename in files:
            wrong_filename = os.path.join(root, wrong_filename)

            number = re.findall(r'\d+', wrong_filename)
            
            if len(wrong_filename) < 4 or wrong_filename[-4:] != ".txt" or len(number) <= 0:
                continue

            if target_number is int(number[0]):
                print(" \033[30mFound at ", wrong_filename, "\033[0m", sep="")
                found = True
                clear = True
                with open(os.path.join(args.target, wrong_filename), "r") as wrong_file:
                    with open(os.path.join(known_directory, correct_filename), "r") as right_file:
                        right_seqs = []
                        wrong_seqs = []

                        for line in right_file:
                            line = [int(n.strip()) for n in line.strip().split(',')]
                            if line:
                                right_seqs.append(line)

                        for line in wrong_file:
                            line = [int(n) for n in re.findall(r'\d+', line)]
                            if len(line) > 0:
                                if line not in right_seqs:
                                    wrong_seqs.append(line)
                                else:
                                    right_seqs.remove(line)
                    
                        wrong_seqs_count = len(wrong_seqs)
                        right_seqs_count = len(right_seqs)

                        if wrong_seqs_count > 0:
                            if wrong_seqs_count > 10:
                                print("\033[31m Added", wrong_seqs_count, "sequences.\033[0m")
                            else:
                                print("\033[31m Added these sequences:", wrong_seqs, "\033[0m")
                            clear = False
                        if right_seqs_count > 0:
                            if right_seqs_count > 10:
                                print("\033[31m Missing", right_seqs_count, "sequences.\033[0m")
                            else:
                                print("\033[31m Missed these sequences:", right_seqs, "\033[0m")
                            clear = False
                        if clear:
                            print("\033[32m Pass.\033[0m")
                            pass

        if found:
            break
    
    if not found:
        print("\033[33m No files generated.\033[0m", sep='')
