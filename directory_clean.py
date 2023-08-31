# File Organizer by File type
# Iterates through present files in directory,
# Organizes them based upin file type in a corresponding
# Folder named after the file type.
#
# Author: Tyler Teufel
# Started Creating: 11/20/22
# Code references: https://www.freecodecamp.org/news/building-bots

#Imports for OS module, and argument parser.
import os
import argparse

parser = argparse.ArgumentParser(
    description= "Clean up directory and put files into corresponding folders."
)

parser.add_argument(
    "--path",
    type=str,
    default=".",
    help="Directory path of the to be cleaned up directory",
)

# parse the arguments given by the user an extract the path
args = parser.parse_args()
path = args.path

print(f"Cleaning up directory {path}")

# get all files from given directory
dir_content = os.listdir(path)

# create a relative path from the path to the file and the document name
path_dir_content = [os.path.join(path, doc) for doc in dir_content]

# filter our directory content into a documents and folders list
docs = [doc for doc in path_dir_content if os.path.isfile(doc)]
folders = [folder for folder in path_dir_content if os.path.isdir(folder)]

# counter to keep track of amount of moved files 
# and list of already created folders to avoid multiple creations
moved = 0
created_folders = []

print(f"Cleaning up {len(docs)} of {len(dir_content)} elements.")


# go through all files and move them into according folders
for doc in docs:
    # separate name from file extension.
    
    full_doc_path, filetype = os.path.splitext(doc)
    doc_path = os.path.dirname(full_doc_path)
    doc_name = os.path.basename(full_doc_path)
    '''
    ' print(filetype)
    ' print(full_doc_path)
    ' print(doc_path)
    ' print(doc_name)
    ''' 
    # skip this file when it is in the directory
    if doc_name == "directory_clean" or doc_name.startswith('.'):
        continue

    # get the subfolder name and create folder if not exist
    subfolder_path = os.path.join(path, filetype[1:].lower())

    #Create Folder, only if it does not already exist.
    if subfolder_path not in folders and subfolder_path not in created_folders:
        try:
            os.mkdir(subfolder_path)
            created_folders.append(subfolder_path)
            print(f"Folder {subfolder_path} created.")
        except FileExistsError as err:
            print(f"Folder already exists at {subfolder_path}... {err}")
    # get the new folder path and move the file
    new_doc_path = os.path.join(subfolder_path, doc_name) + filetype

    #
    os.rename(doc, new_doc_path)
    moved += 1
    
    print(f"Moved file {doc} to {new_doc_path}")
    
print(f"Moved {moved} files in this directory into corresponding folders.")
