from __future__ import print_function
import httplib2
import os
import io

from apiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name('project.json', SCOPES)
CLIENT_SECRET_FILE = 'project.json'
APPLICATION_NAME = 'File Downloader'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    #credential_path = "./client_secret.json"
    credential_path = os.path.join(credential_dir,'file-downloader.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    file_list = {}
    children = service.files().list(q='"zyYm8" in parents').execute()
    for file in children.get('files', []):
        print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        id = file.get('id')
        name = file.get('name')
        file_list[id] = name

    for k,name in file_list.items():
        curr_file = service.files().export_media(fileId=k, mimeType='application/pdf')#.execute()
        fh = io.FileIO("tmp/"+name,"wb")

        downloader = MediaIoBaseDownload(fh, curr_file)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))

if __name__ == '__main__':
    main()
