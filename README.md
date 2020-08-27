# Code
1: Success
0: Error

# If you want sub-folders inside folders to move to new directory as well
folder_unzip = False
# If you want empty folders to be removed after moving files to new directory
delete_empty_folders_var = True

# Command-line:
1. -i: input_path where files are residing.
It is mandatory.
2. -o: output_path.
If not entered, will be equal to input path.
3. -t: task which could be:-
        3a) pack: to pack the files in folder
        3b) unpack: to unpack the files from folder
        3c) repack: to unpack the files first and then pack again in different bundle
4. -b: bundle size is the no of files to be put in each folder.
It is mandatory for task value pack and repack
5. -del: If used, it will remove empty folders from the input directory.
6. -u: If you want the sub-folders to be moved to new path or unpack along with files.

# Example of commands:

python execute.py -u -del -i C:\Deep_Learning_RULA\FullBodyDataset\test -o C:\Deep_Learning_RULA\FullBodyDataset\test_1 -t pack -b 5
