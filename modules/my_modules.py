import os
import glob

class General:
    def __init__(self):
        pass

    def delete_logs(path, keep):
        """
        Function for deleting automatically logs from a path, keeping only the number of logs specified.
        No logs will be deleted if there are less for those to keep.
        """
        logs = glob.glob(path) # Path and log pattern of the folder that stores the logs
        sorted_logs = sorted(logs, key=os.path.getmtime, reverse=True)

        if len(sorted_logs) <= keep:
            print(f"No logs to delete. In folder: {len(sorted_logs)}. To keep: {keep}.")
        else:
            for i in range(len(sorted_logs)):
                if i > keep:
                    try:
                        os.remove(sorted_logs[i])
                        print(f"Log '{sorted_logs[i]}' deleted.")
                    except Exception as e:
                        print(f"Could not delete log '{sorted_logs[i]}'.")

class Melee:
    start_gg_api = "HERE_GOES_YOUR_START_GG_API"

    query_tournament = """
        query tournamentsRD {
        tournaments(query: {
            filter: {
            countryCode: "DO" # Dominican Republic
            videogameIds: [
                1
            ] # Super Smash Bros Melee
            }
        }) {
            nodes {
            events {
                id
                type
                videogame {
                id
                }
            }
            }
        }
        }
    """

    query_online_tournament = """
        query tournamentsRD {{
        tournaments(query: {{
            filter: {{
            ownerId: {id}
            videogameIds: [
                1
            ] # Super Smash Bros Melee
            }}
        }}) {{
            nodes {{
            events {{
                id
                type
                videogame {{
                id
                }}
            }}
            }}
        }}
        }}
    """

    query_events = """
        query GetEventById {{
        event(id: {id}) {{
            id
            name
            startAt
            slug
            tournament {{
            name
            isOnline
            }}
            standings(query: {{perPage : 3}}) {{
            nodes {{
                placement
                entrant {{
                name
                }}
            }}
            }}
        }}
        }}
    """


class Sheets:
    service_account_file = "/path/to/my/service_account_file.json"
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    def dr_tournaments():
        """
        Function that returns the spreadsheets ID of the project.
        Offline, Online.
        """
        return "SPREADSHEET_ID", "SPREADSHEET_ID_ONLINE"