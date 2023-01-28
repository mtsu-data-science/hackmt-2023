import os
import csv
import shutil

# path to the folder containing the csvs
folder_path = os.getcwd() + '/'

# path to the folder where the parsed csvs will be stored
parsed_folder_path = 'Parsed-Subreddits/'

# check if the parsed folder already exists, if not create it
if not os.path.exists(parsed_folder_path):
    os.makedirs(parsed_folder_path)

# loop through all the files in the folder
for filename in os.listdir(folder_path):
    # check if the file is a csv
    if filename.endswith(".csv"):
        # move the csv file to the parsed folder
        shutil.move(folder_path + filename, parsed_folder_path + filename)
        print(f'{filename} moved to {parsed_folder_path}')
    else:
        print(f'{filename} is not a csv')
