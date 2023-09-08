"""
Author: Jordan Angus @CL_Projects
Version: Python 3.9
Description: This program downloads a file from a url passed as an argument or the default example file. 
Its final actions compiles and runs a separate program.
"""
import requests
import sys
import os

# URL of the file to download
url = 'http://example.com/file-to-download.txt'
try:
    url = sys.argv[1]
except:
    None

# Path to this folder should be the same as the location of all other file/programs expected; ~/ may throw a permissions error
downloads_folder = os.getcwd()

# Creates download folder if it doesn't exist
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

# Determines file name from last part of the URL
file_name = url.split('/')[-1]

# Combines folder and file name to get the full path
file_path = os.path.join(downloads_folder, file_name)
#print(file_path)
# Download the file and save it
try:
    response = requests.get(url)
except:
    print("Error: Invalid url...")
    exit()

with open(file_path, 'wb') as f:
    f.write(response.content)

print('File downloaded and saved to ', file_path)

#os.chdir(file_path)
command = "./c_c " + file_name
os.system("gcc -Wall -Wextra -O2 -g -o c_c c_c.c")
os.system(command)
exit()