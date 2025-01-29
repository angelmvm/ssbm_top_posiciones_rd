import requests
import sys
import pandas as pd
from time import strftime, localtime, sleep
from datetime import datetime as dt
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

sys.path.append("/home/user/scripts/modules")
from my_modules import Melee, Sheets

# Path to your service account key file
SERVICE_ACCOUNT_FILE = Sheets.service_account_file

# Scopes for Google Sheets API
SCOPES = Sheets.scopes

# Authenticate and initialize the Sheets API
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# Your Google Sheet ID and range
SPREADSHEET_ID, SPREADSHEET_ID_ONLINE = Sheets.dr_tournaments()
RANGE = 'Sheet1!A1'

api_start_gg = Melee.start_gg_api
tournament_query = Melee.query_tournament
online_tournament_query = Melee.query_online_tournament
event_query = Melee.query_events

dt_format = "%Y-%m-%d %H:%M:%S"

def get_data(api_key, query, event=None):
    """Function used for getting data from Start GG API."""
    sleep(15)
    url = "https://api.start.gg/gql/alpha"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    if event == None:
        response = requests.post(url, headers=headers, json={"query": query})
    else:
        response = requests.post(url, headers=headers, json={"query": query.format(id = event)})

    if response.status_code == 200:
        data = response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {response.text}")

    return data

def main():
    print(f"[{dt.now().strftime(dt_format)}]: Getting offline tournament data...")
    tournament_data = get_data(api_start_gg, tournament_query)
    tournament_list = tournament_data["data"]["tournaments"]["nodes"]
    event_list = []
    for i in range(len(tournament_list)):
        for j in range(len(tournament_list[i]["events"])):
            event_type_id = tournament_list[i]["events"][j]["type"]
            event_game_id = tournament_list[i]["events"][j]["videogame"]["id"]
            if event_game_id == 1 and event_type_id == 1:
                event_list.append(tournament_list[i]["events"][j]["id"])

    event_id = []
    tournament_name = []
    event_name = []
    event_date = []
    first_place = []
    second_place = []
    third_place = []
    event_url = []

    for i in range(len(event_list)):
        event_data = get_data(api_start_gg, event_query, event_list[i])
        # Special and online tournaments filtered out
        if len(event_data["data"]["event"]["standings"]["nodes"]) != 0 and event_data["data"]["event"]["id"] != 1002043 and event_data["data"]["event"]["tournament"]["isOnline"] == False:
            print(f"[{dt.now().strftime(dt_format)}]: Getting data of tournament {event_data['data']['event']['tournament']['name']}...")
            event_id.append(event_data["data"]["event"]["id"])
            tournament_name.append(event_data["data"]["event"]["tournament"]["name"])
            event_name.append(event_data["data"]["event"]["name"])
            event_date.append(strftime('%Y-%m-%d %H:%M', localtime(event_data["data"]["event"]["startAt"])))
            first_place.append(event_data["data"]["event"]["standings"]["nodes"][0]["entrant"]["name"])
            second_place.append(event_data["data"]["event"]["standings"]["nodes"][1]["entrant"]["name"])
            third_place.append(event_data["data"]["event"]["standings"]["nodes"][2]["entrant"]["name"])
            event_url.append("https://www.start.gg/" + event_data["data"]["event"]["slug"])
    
    print(f"[{dt.now().strftime(dt_format)}]: Tabulating offline tournaments data...")
    df = pd.DataFrame({
        "id_evento" : event_id,
        "nombre_torneo" : tournament_name,
        "nombre_evento" : event_name,
        "fecha_evento" : event_date,
        "primer_lugar" : first_place,
        "segundo_lugar" : second_place,
        "tercer_lugar" : third_place,
        "url_evento" : event_url
        })

    # Format required for Google Standard
    data = [df.columns.tolist()] + df.values.tolist()

    # Prepare the request body
    body = {
        'values': data
    }

    print(f"[{dt.now().strftime(dt_format)}]: Writing to Google Sheets...")
    # Write data to the spreadsheet
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"[{dt.now().strftime(dt_format)}]: {result.get('updatedCells')} cells updated for offline events.")
    except Exception as e:
        print(f"[{dt.now().strftime(dt_format)}]: Error writing offline tournaments data to Google Sheets. Error: {e}")

    # Online tournaments
    def online(owner_id):
        online_tournament_data = get_data(api_start_gg, online_tournament_query.format(id = owner_id))
        online_tournament_list = online_tournament_data["data"]["tournaments"]["nodes"]
        online_event_list = []
        for i in range(len(online_tournament_list)):
            for j in range(len(online_tournament_list[i]["events"])):
                online_event_type_id = online_tournament_list[i]["events"][j]["type"]
                online_event_game_id = online_tournament_list[i]["events"][j]["videogame"]["id"]
                if online_event_game_id == 1 and online_event_type_id == 1:
                    online_event_list.append(online_tournament_list[i]["events"][j]["id"])

        online_event_id = []
        online_tournament_name = []
        online_event_name = []
        online_event_date = []
        online_first_place = []
        online_second_place = []
        online_third_place = []
        online_event_url = []

        for i in range(len(online_event_list)):
            online_event_data = get_data(api_start_gg, event_query, online_event_list[i])
            # Special and online tournaments filtered out
            if len(online_event_data["data"]["event"]["standings"]["nodes"]) != 0 and online_event_data["data"]["event"]["id"] != 1002043 and online_event_data["data"]["event"]["tournament"]["isOnline"] == True:
                print(f"[{dt.now().strftime(dt_format)}]: Getting data of tournament {online_event_data['data']['event']['tournament']['name']}...")
                online_event_id.append(online_event_data["data"]["event"]["id"])
                online_tournament_name.append(online_event_data["data"]["event"]["tournament"]["name"])
                online_event_name.append(online_event_data["data"]["event"]["name"])
                online_event_date.append(strftime('%Y-%m-%d %H:%M', localtime(online_event_data["data"]["event"]["startAt"])))
                online_first_place.append(online_event_data["data"]["event"]["standings"]["nodes"][0]["entrant"]["name"])
                online_second_place.append(online_event_data["data"]["event"]["standings"]["nodes"][1]["entrant"]["name"])
                online_third_place.append(online_event_data["data"]["event"]["standings"]["nodes"][2]["entrant"]["name"])
                online_event_url.append("https://www.start.gg/" + online_event_data["data"]["event"]["slug"])
        
        print(f"[{dt.now().strftime(dt_format)}]: Tabulating online tournaments data...")
        online_df = pd.DataFrame({
            "id_evento" : online_event_id,
            "nombre_torneo" : online_tournament_name,
            "nombre_evento" : online_event_name,
            "fecha_evento" : online_event_date,
            "primer_lugar" : online_first_place,
            "segundo_lugar" : online_second_place,
            "tercer_lugar" : online_third_place,
            "url_evento" : online_event_url
            })
        
        return online_df

    leof_events = online("95274") # Leof's ID
    zell_events = online("1243015") # Zell's ID
    zuraco_events = online("205330") # Zuraco's ID

    print(f"[{dt.now().strftime(dt_format)}]: Joining online tournament data...")
    all_df = pd.concat([leof_events, zell_events, zuraco_events], ignore_index=True)

    # Format required for Google Standard
    online_data = [all_df.columns.tolist()] + all_df.values.tolist()

    # Prepare the request body
    online_body = {
        'values': online_data
    }

    print(f"[{dt.now().strftime(dt_format)}]: Writing to Google Sheets...")
    # Write data to the spreadsheet
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID_ONLINE,
            range=RANGE,
            valueInputOption='RAW',
            body=online_body
        ).execute()
        print(f"[{dt.now().strftime(dt_format)}]: {result.get('updatedCells')} cells updated for online events.")
    except Exception as e:
        print(f"[{dt.now().strftime(dt_format)}]: Error writing online tournaments data to Google Sheets. Error: {e}")

if __name__ == "__main__":
    print(f"[{dt.now().strftime(dt_format)}]: Script started.")
    main()
    print(f"[{dt.now().strftime(dt_format)}]: Script finished.")