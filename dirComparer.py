#!/usr/bin/env python3
import os
import argparse

def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='dirComparer',
        description="Compares that no files are missing or incomplete, only checks for size, no hashing"
    )
    parser.add_argument('orig_dir')
    parser.add_argument('dest_dir')

    return parser.parse_args()


def print_colored(text, color=None, bold=False):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'end': '\033[0m'  # Reset to default color
    }
    bold_code = '\033[1m' if bold else ''
    end_code = '\033[0m'
    
    if color in colors:
        print(f"{bold_code}{colors[color]}{text}{end_code}")
    else:
        print(f"{bold_code}{text}{end_code}")


def compare_dir_contents(dir1, dir2):
    dir1_files = {os.path.relpath(path, dir1) for path in list_files(dir1)}
    dir2_files = {os.path.relpath(path, dir2) for path in list_files(dir2)}

    missing_in_dir2 = set(dir1_files) - set(dir2_files)
    missing_in_dir1 = set(dir2_files) - set(dir1_files)

    print_colored(f"Files missing in {dir2}:", bold=True)
    for file in missing_in_dir2:
        print_colored(f"-{file}", "red")

    print_colored(f"\nAdditional files only existing in {dir2}:", bold=True)
    for file in missing_in_dir1:
        print_colored(f"+{file}", "green")


def find_incomplete_files(dir1, dir2):
    dir1_files = list_files(dir1)
    dir2_files = list_files(dir2)

    dir1_dict = {os.path.basename(path): os.path.getsize(path) for path in dir1_files}
    dir2_dict = {os.path.basename(path): os.path.getsize(path) for path in dir2_files}

    common_files = set(dir1_dict.keys()) & set(dir2_dict.keys())

    incomplete_files = [
        file
        for file in common_files
        if dir2_dict[file] < dir1_dict[file]
    ]

    print_colored("Partially copied files:", bold=True)
    for file in incomplete_files:
        print_colored(f"~{file}", "yellow")


def main():
    args = setup_parser()

    dir1 = args.orig_dir
    dir2 = args.dest_dir

    compare_dir_contents(dir1, dir2)
    
    print("\n")

    find_incomplete_files(dir1, dir2)


if __name__ == "__main__":
    main()
