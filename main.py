import click
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = ''
RANGE_NAME = 'Sheet1!A2:E'


store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)


@click.group()
def cli():
    return None

@cli.command()
def update_existing_show():
    service = build('sheets', 'v4', http=creds.authorize(Http()))



@cli.command()
def update_new_show():

    service = build('sheets', 'v4', http=creds.authorize(Http()))
    name = input('Series name: ')
    release_year = input('Year of release: ')
    termination_year = input('Year it ended: ')
    options = {
        1: 'Yet to watch',
        2: 'Watching',
        3: 'Finished watching :(',
    }
    click.echo('Options: ')
    for option in options.items():
        print("Type", option[0], "to set status as:", option[1])

    status = int(input('Status: '))
    if status not in options.keys():
        raise ValueError('Invalid option selected')

    if options[status] == options[2]:
        season = input("Which season are you watching? ")
        episode = input("Which episode are you watching? ")
        final_status = 'S{}E{}'.format(season, episode)
    else:
        final_status = options[status]

    rating = input('What would you rate it? ')
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    id_ = len(result.get('values', [])) + 1
    values = [
        [
            id_, name, release_year, termination_year, final_status, float(rating) if rating else ''
        ]
    ]
    body = {
        'values': values
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=body).execute()

@cli.command()
def get():

    service = build('sheets', 'v4', http=creds.authorize(Http()))

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[1], row[4]))
