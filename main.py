import json

import click
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)


@click.group()
def cli():
    return None


@cli.command('update_existing')
def update_existing_show():

    spreadsheet = _choose_spreadsheet()
    SPREADSHEET_ID = spreadsheet[0]
    RANGE_NAME = spreadsheet[1]

    service = build('sheets', 'v4', http=creds.authorize(Http()))


@cli.command('update_new')
def update_new_show():

    spreadsheet = _choose_spreadsheet()
    SPREADSHEET_ID = spreadsheet[0]
    RANGE_NAME = spreadsheet[1]

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
    genre = input('Genre of the series? ')
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    id_ = len(result.get('values', [])) + 1
    values = [
        [
            id_,
            name,
            release_year if release_year else 'N/A',
            termination_year if termination_year else 'N/A',
            final_status,
            float(rating) if rating else 'N/A',
            genre if genre else 'N/A'
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

    spreadsheet = _choose_spreadsheet()
    SPREADSHEET_ID = spreadsheet[0]
    RANGE_NAME = spreadsheet[1]

    service = build('sheets', 'v4', http=creds.authorize(Http()))

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:

        print(
            '{:<4} | {:<40} | {:<17} | {:<20} | {:<26} | {:<8} | {:<30}'
            .format(
                    'ID',
                    'Name',
                    'Year of release',
                    'Year of truncation',
                    'Seasons/Episodes watched',
                    'Rating',
                    'Genre'
            )
        )
        for row in values:
            print(
                '{:<4} | {:<40} | {:<17} | {:<20} | {:<26} | {:<8} | {:<30}'
                .format(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5] if row[5] else '',
                    row[6] if row[6] else ''
                )
            )


SPREADSHEET_ID = ''
RANGE_NAME = ''


def _choose_spreadsheet():
    with open('spreadsheets.json') as f:
        content = json.load(f)
        for result in content['spreadsheets']:
            print("{} : {}".format(result['serial_no'], result['name']))

        serial = int(input("Choose your spreadsheet: "))
        for result in content['spreadsheets']:
            if result['serial_no'] == serial:
                SPREADSHEET_ID = result['creds']['id']
                RANGE_NAME = result['creds']['range']
                return SPREADSHEET_ID, RANGE_NAME