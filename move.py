import os
import sys
import shutil

import argparse

def make_new_dir(dir_name:str) -> None:
    if dir_name not in os.listdir():
        os.mkdir(dir_name)

def prepare_file_list() -> list:
    full_file_list = os.listdir()
    this_file = sys.argv[0]
    full_file_list.remove(this_file)
    return full_file_list

def move_files_to_dir(dirname:str, file_list:list) -> None:
    move_template = '{dirname}_{file_name}'
    for file in file_list:
        shutil.move(file, move_template.format(dirname=dirname, file_name=file))

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirname')
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    make_new_dir(args.dirname)
    file_list = prepare_file_list()
    move_files_to_dir(dirname=args.dirname, file_list=file_list)

if __name__ == '__main__':
    main()
