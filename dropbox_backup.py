from zipfile import ZipFile
import os
import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError
import config

def backup(TOKEN,LOCALFILE,BACKUPPATH):
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid

    dbx.users_get_current_account()
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                sys.exit()
            else:
                sys.exit()
def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

            # returning all file paths
    return file_paths


def main(files,token):
    # path to folder which needs to be zipped
    directory = './'+files

    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(directory)

    # printing the list of all files to be zipped
    for file_name in file_paths:
        pass
    files = files + '.zip'
        # writing files to a zipfile
    with ZipFile(files, 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)

    backup(token,files,'/'+files)

for x in range(len(config.files)):
    main(config.files[x],config.token)
    os.remove(config.files[x]+'.zip')