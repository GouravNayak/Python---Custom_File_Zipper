# code
# 1: Success
# 0: Error

# if you want sub-folders inside folders to move to new directory as well
folder_unzip = False
# if you want empty folders to be removed after moving files to new directory
delete_empty_folders_var = True

command-line:

python execute.py -u -del -i C:\Deep_Learning_RULA\FullBodyDataset\test -o C:\Deep_Learning_RULA\FullBodyDataset\test_1 -t pack -b 5
