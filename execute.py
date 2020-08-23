import os
import argparse

execute_parser = argparse.ArgumentParser(description='', allow_abbrev=False)

execute_parser.add_argument("-i", "--input", required=True,
                            help="path to input directory")
execute_parser.add_argument('-t', '--task', choices=['pack', 'unpack', 'repack'], required=True,
                            help='task that needs to be performed. Can be pack, unpack or repack')

execute_parser.add_argument("-o", "--output",
                            help="path to output directory")

execute_parser.add_argument('-u', '--folder_unzip', action='store_false',
                            help='if you want sub-folders inside folders to move to new directory as well')

execute_parser.add_argument('-del', '--delete_empty_folders_var', action='store_true',
                            help='if you want empty folders to be removed after moving files to new directory')

execute_parser.add_argument('-b', '--file_bundle', action='store', type=int,
                            help='number of files in each folder')
args = execute_parser.parse_args()

if vars(args)['output'] is None:
    print('Output directory not specified. Setting it equal to source directory')
    vars(args)['output'] = args.input

if vars(args)['task'] is None and vars(args)['task'] in ['pack', 'repack']:
    execute_parser.error('For -task argument pack or repack program requires --file_bundle or -b argument')

print(args.input)
print(args.folder_unzip)
print(args.task)
print(args.delete_empty_folders_var)

# src_test_path = r'C:\Deep_Learning_RULA\FullBodyDataset\test_1'
src_test_path = args.input
# destination_test_path = r'C:\Deep_Learning_RULA\FullBodyDataset\test'
destination_test_path = args.output
# if you want sub-folders inside folders to move to new directory as well
# folder_unzip = True
folder_unzip = args.folder_unzip
# if you want empty folders to be removed after moving files to new directory
# delete_empty_folders_var = True
delete_empty_folders_var = args.delete_empty_folders_var
# file_bundle = 5
file_bundle = args.file_bundle


def check_directory_path(run_path):
    print('Validating directory path')
    if os.path.exists(run_path):
        print('Valid path: ' + str(run_path))
        message = ''
        return message, 1
    else:
        message = ''
        return message, 0


# Use-Case 4: pack files into folders
# bundle_count denotes the no of files needed in one folder
def pack_files_to_directory(source_path, destination_path, bundle_count):
    # check if directories are valid
    source_status_message, source_status_code = check_directory_path(source_path)
    destination_status_message, destination_status_code = check_directory_path(destination_path)

    if source_status_code == 0:
        return source_status_message, 0
    if destination_status_code == 0:
        return destination_status_message, 0

    success_message = ''
    status_code = 1
    if source_path == destination_path:
        print('Same directory operations')
    else:
        print('Packing to different directories')
    file_path_list = []

    # Retrieve the path of files to be bundled
    for dirName, subDirList, fileList in os.walk(source_path):
        if dirName == source_path:
            if len(fileList) == 0:
                print('All files are bundled')
                return success_message, status_code
            else:
                print('Total no of files to be zipped: ' + str(len(fileList)))
                for file_name in fileList:
                    file_name_path = str(dirName)+str('\\')+str(file_name)
                    file_path_list.append(file_name_path)
    # count total folders required for bundling
    folder_count = len(file_path_list)/bundle_count
    if folder_count.is_integer():
        folder_count = int(folder_count)
    else:
        folder_count = int(folder_count)+1
    print('Total no of folders to be created: ' + str(folder_count))

    for folder_counter in range(folder_count):
        new_folder_dir = str(destination_path) + str('\\') + str(folder_counter)
        print('Creating Folder: ' + str(new_folder_dir))
        # create folders if not exist already
        if not os.path.exists(new_folder_dir):
            os.mkdir(new_folder_dir)
        for bundle_counter in range(0, bundle_count):
            # find the index of files to be moved in the folder
            file_path_list_index = (folder_counter*bundle_count) + bundle_counter
            # check to avoid error if last bundle size is greater than available files
            if file_path_list_index < len(file_path_list):
                # Move a file by renaming it's path
                current_file_path = str(file_path_list[file_path_list_index]).rsplit('\\',1)[1]
                new_path = str(new_folder_dir) + str('\\') + str(current_file_path)
                old_path = file_path_list[file_path_list_index]
                print('Moving file at : ' + str(new_path))
                os.rename(old_path, new_path)
    print('Directory move finished')
    return success_message, status_code


# Use Case 1: Check if files are inside or outside the folder
def files_pack_status(source_path, destination_path, bundle_count):
    if bundle_count is None or bundle_count < 0:
        print('Files to be bundles could not be negative')
        return 0
    if bundle_count > 0:
        for src_dir_name, src_subDir_names, src_file_names in os.walk(source_path):
            if len(src_file_names) == 0:
                print('No files outside folders')
                return 1
            elif len(src_file_names) >= bundle_count:
                print('Files outside the folders')
                return 1
            else:
                # len(src_file_names)< bundle_count
                print('Files outside the folders are less than entered bundle count')
                return 2
    if bundle_count == 0:
        print('Calling unpack_files')
        unpack_files(source_path, destination_path)


# Use case 2: Un-zip files and sub-folders from folders
def unpack_files(source_path, destination_path):
    # check if directories are valid
    source_status_message, source_status_code = check_directory_path(source_path)
    destination_status_message, destination_status_code = check_directory_path(destination_path)

    if source_status_code == 0:
        return source_status_message, 0
    if destination_status_code == 0:
        return destination_status_message, 0

    success_status_message = ''
    success_status_code = 1
    if source_path == destination_path:
        print('Same directory operations')
    else:
        print('Un-packing to different directories')

    # check if any folders are available in source directory to unzip
    list_of_folder_paths = []
    list_of_sub_folder_paths = []
    list_of_file_names_path = []
    list_of_folder_names_path= []
    for src_dir_name, src_subDir_names, src_file_names in os.walk(source_path):
        # Working on the parent path
        if src_dir_name == source_path:
            print('In the root folder')
            # check if there are folders to be unzipped
            if len(src_subDir_names) == 0:
                print('No folders to be unzipped')
                success_status_message = ''
                return success_status_message, 1
            else:
                # path of all the folders in the root path
                for src_subDir_name in src_subDir_names:
                    src_zip_folder_path = ''
                    src_zip_folder_path = str(src_dir_name) + str('\\') + str(src_subDir_name)
                    # store the folder names to be unzipped
                    list_of_folder_paths.append(src_zip_folder_path)
                # break
            print('Number of folders to be unzipped: ' + str(len(list_of_folder_paths)))
            # walk through each folder and unzip it
            if len(list_of_folder_paths) > 0:
                for folder_path in list_of_folder_paths:
                    print('Collecting file paths: '+str(folder_path))
                    for src_folder_dir_name, src_folder_subDir_names, src_folder_file_names in os.walk(folder_path):
                        # check if folders have files in them to move
                        if src_folder_dir_name == folder_path:
                            if len(src_folder_file_names) > 0:
                                for src_folder_file_name in src_folder_file_names:
                                    src_folder_file_path = str(src_folder_dir_name) + str('\\') \
                                                           + str(src_folder_file_name)
                                    # store all the file paths
                                    list_of_file_names_path.append(src_folder_file_path)
                            # check if folders have sub-folders in them to move and flag is true
                            if len(src_folder_subDir_names) > 0 and folder_unzip:
                                for src_folder_sub_folder_name in src_folder_subDir_names:
                                    src_folder_sub_folder_path = str(src_folder_dir_name) + str('\\') + \
                                                                 str(src_folder_sub_folder_name)
                                    # store all the file paths
                                    list_of_folder_names_path.append(src_folder_sub_folder_path)

                print('Total no of files to be moved: ' + str(len(list_of_file_names_path)))
                # start unzipping the files
                for file_name_path in list_of_file_names_path:
                    print('UnZipping: '+str(file_name_path))
                    file_name = file_name_path.rsplit('\\', 1)[1]
                    new_path = str(destination_path) + str('\\') + str(file_name)
                    old_path = str(file_name_path)
                    os.rename(old_path, new_path)

                print('Total no of folders to be moved: ' + str(len(list_of_folder_names_path)))
                # start unzipping the folders
                for folder_name_path_item in list_of_folder_names_path:
                    print('UnZipping: '+str(folder_name_path_item))
                    folder_name_path = folder_name_path_item.rsplit('\\', 1)[1]
                    new_path = str(destination_path) + str('\\') + str(folder_name_path)
                    old_path = str(folder_name_path_item)
                    os.rename(old_path, new_path)

        else:
            for src_subFolder_dir_name, src_subFolder_subDir_names, src_subFolder_file_names in os.walk(src_dir_name):
                # if len(src_subFolder_subDir_names) > 0:
                #     print('Sub-Folders detected inside Folders: '+str(src_dir_name))
                #     for src_subFolder_subDir_name in src_subFolder_subDir_names:
                #         sub_dir_folder_path = str(src_subFolder_dir_name) + str('\\') + str(src_subFolder_subDir_name)
                #         list_of_sub_folder_paths.append(sub_dir_folder_path)
                #
                # if folder_unzip:
                #     print('No of sub-folders detected: ' + str(len(list_of_sub_folder_paths)))
                #     for sub_folder_path in list_of_sub_folder_paths:
                #         sub_folder_name = sub_folder_path.rsplit('\\', 1)[1]
                #         new_sub_folder_path = str(destination_path) + '\\' + str(sub_folder_name)
                #         print('Moving folder: ' + str(sub_folder_path))
                #         os.rename(sub_folder_path, new_sub_folder_path)
                #         print('New Path: ' + str(new_sub_folder_path))

                if delete_empty_folders_var:
                    print('Checking for empty folder: '+str(src_dir_name))
                    delete_empty_folders(src_dir_name)

    return success_status_message, success_status_code


# Use-case 3: Delete empty folders
def delete_empty_folders(source_folder_path):
    for src_dir_name, src_subDir_names, src_file_names in os.walk(source_folder_path):
        # checking for files and folders
        if len(src_subDir_names) == 0 and len(src_file_names) == 0:
            print('Deleting Empty folder: '+str(src_dir_name))
            # rmdir removes only empty folders
            os.rmdir(src_dir_name)
        else:
            print('Folder is not empty')


# Use-case 5: Un-bundle the files and then bundle with another bundle count
def re_pack_files_to_directory(source_path, destination_path, re_bundle_count):
    success_status_message = ''
    success_status_code = 1
    # un-pack the files
    unpack_success_status_message, unpack_success_status_code = unpack_files(source_path, destination_path)
    # pack the files
    pack_success_status_message, pack_success_status_code = pack_files_to_directory(destination_path,
                                                                                    destination_test_path,
                                                                                    re_bundle_count)

    return success_status_message, success_status_code


if args.task == 'unpack':
    unpack_status_message, unpack_status_code = unpack_files(src_test_path, destination_test_path)
    if unpack_status_code == 0:
        print('Failed')
if args.task == 'pack':
    pack_status_message, pack_status_code = pack_files_to_directory(src_test_path, destination_test_path, file_bundle)
    if pack_status_code == 0:
        print('Failed')
if args.task == 'repack':
    re_pack_status_message, re_pack_status_code = re_pack_files_to_directory(src_test_path, destination_test_path, file_bundle)
    if re_pack_status_code == 0:
        print('Failed')

