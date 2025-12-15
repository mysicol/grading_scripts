from argparse import ArgumentParser
import os

parser = ArgumentParser(description="Add makefile targets to automatically generate larger sequences.")
parser.add_argument("gradebook", type=str, help="gradebook directory", default=".")
args = parser.parse_args()

# parse all subdirectories to find makefiles
for root, subdirectory, files in os.walk(args.gradebook):
    # specifically find makefiles
    for filename in files:
        if filename.lower() == "makefile":
            lines = ""
            filepath = os.path.join(root, filename)
            print("Makefile found at", filepath)

            with open(filepath, 'r') as file:
                lines = file.readlines()
                new_lines = []
                newt_lines = lines.copy()

                for i in range(len(lines)):
                    line = lines[i]
                    found_test7 = False

                    if "test7:" in line:
                        found_test7 = True
                        make_commands = ["\n", line]

                        while lines[i+1][0] == "\t":
                            make_commands.append(lines[i+1])
                            i+=1

                        with open(filepath, 'a') as file:
                            file.writelines(["\n"])
                            for n in [3, 5, 15, 17, 19]:
                                new_commands = []
                                for line in make_commands:
                                    new_commands.append(line.replace("7", str(n)))
                                file.writelines(new_commands)
                        
                            file.writelines("\nrun: test3 test5 test7 test9 test11 test13 test15 test17")

                        break
                if found_test7:
                    print(" \033[32m Success.\033[0m")
                else:
                    print(" \033[31m No tests found.\033[0m")