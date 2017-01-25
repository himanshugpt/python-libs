from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import dateutil.parser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret_calendar.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


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
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
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
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()

    to_avoid = ['Techops Tuesdays Seamless lunch', '*Reminder* place your seamless order', 'No Meetings, No Interviews','Skunkworks',
    'WFH']
    
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    quarterEnd = datetime.datetime(year=2017,month=4,day=30).isoformat() + 'Z'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, 
        timeMax=quarterEnd, singleEvents=True,
        orderBy='startTime')
    .execute()
    events = eventsResult.get('items', [])
    td = datetime.timedelta()
    if not events:
        print('No upcoming events found.')
    for event in events :
        if event['summary'] not in to_avoid:
            print (event['summary'])
            start = event['start'].get('dateTime')#, event['start'].get('date'))
            st = dateutil.parser.parse(start)
            end = event['end'].get('dateTime')
            ed = dateutil.parser.parse(end)
            duration = ed - st
            td = td+duration
            #startDateTime = 
            print(start, end, duration)
    print (td)


if __name__ == '__main__':
    main()