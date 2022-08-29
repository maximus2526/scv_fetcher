import csv
import json
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_from_google_drive():
    """
    Authorization of the service client
    Download file
    :return: request
    """
    file_id = '1zLdEcpzCp357s3Rse112Lch9EMUWzMLE'
    scope = ['https://www.googleapis.com/auth/drive.readonly']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'gdrive_access/employees_secret.json',
        scope
    )
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id).execute()
    return request


def csv_to_json(data):
    """
    Converting csv to json
    Files are created for processing
    :param data:
    """

    with open('data_storage/file.csv', 'w') as csv_f:
        json_array = []
        csv_f.write(data.decode())

    with open('data_storage/file.csv', 'r') as csv_f:
        csv_reader = csv.DictReader(csv_f.readlines(), delimiter=',')
        # convert each csv row into python dict
        for row in csv_reader:
            # add this python dict to json array
            json_array.append(row)
    # convert python jsonArray to JSON String and write to file
    with open('data_storage/data.json', 'w', encoding='utf-8') as json_f:
        json_string = json.dumps(json_array, indent=4)
        json_f.write(json_string)
        line_selection(json_string)


def line_selection(json_data):
    """
    Handle lines from command line
    Client should select some rows
    :return: result
    """
    # lines = sys.argv[1:] # ЦЕ МАЄ БУТИ
    lines = ['date', 'clicks', 'source'] # Заглушка
    if len(lines) == 0:  # if no have command - print all json
        print(json_data)
        return
    result = {'data': None}
    json_data = json.loads(json_data)
    list_of_dicts = []
    temp_dict = dict()
    for row in json_data:
        for line in lines:
            if line in row.keys():
                temp_dict[line] = row[line]
        list_of_dicts.append(temp_dict)

    result['data'] = list_of_dicts
    result = json.dumps(result, indent=4)
    print(result)


def wait_for_changes(data):
    """
    Check of change data in the gdrive
    :return: Some changes
    """


if __name__ == '__main__':
    csv_to_json(get_from_google_drive())
