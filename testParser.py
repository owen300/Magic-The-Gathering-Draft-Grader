import re
import json
import ijson#enables faster reads
import os
filename='user_data.json'
class logHandler:
    #get the cards drafted and the amount of each, in an array
    def extract_card_data(file_path):
        with open(file_path, 'r') as file:
          log_data = file.read()

        
        match = re.search(r'Event_SetDeckV2.*?({.*})', log_data)
        if not match:
            print("No deck data found.")
            return
    
        
        json_data = match.group(1)
    
        
        try:
            deck_data = ijson.loads(ijson.loads(json_data)["request"])
            main_deck = deck_data["Deck"].get("MainDeck", [])
            sideboard = deck_data["Deck"].get("Sideboard", [])
        
            
            all_cards = main_deck + sideboard

            arr=[]
            for card in all_cards:
                arr.append([card['cardId'],card['quantity']])
            return(arr)
        except ijson.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    def __init__(self):
        #Initialize the log handler with a JSON file.
    
        self.initialize_json()

    def initialize_json(self):
        ##Check if the JSON file exists; if not, create an empty JSON structure.
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                json.dump({}, file)  # ijson isn't used for initialization
            print(f"Initialized file '{filename}'.")
        else:
            print(f"File '{filename}' already exists.")

    def add_user_data(self, username=None, data=None):
        if username is None or data is None:
            print("Username and data must be provided.")
            return

        # Read existing content incrementally using ijson
        content = {}
        try:
            with open(filename, 'r') as file:
          
                content = {key: value for key, value in ijson.kvitems(file, '')}
        except (ijson.JSONDecodeError, FileNotFoundError):
            print("JSON file is empty, corrupted, or does not exist. Initializing a new file.")
            self.initialize_json()

        if username not in content:
            content[username] = []

        if data in content[username]:
            print(f"Data '{data}' already exists for user '{username}'.")
            return
        else:
            content[username].append(data)
            print(f"Data '{data}' added for user '{username}'.")

        try:
            with open(filename, 'w') as file:
                json.dump(content, file, indent=4)
            print(f"Data saved successfully for user '{username}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def get_user_logs(self):
        #Retrieve and print logs for all users incrementally using ijson.
        try:
            with open(filename, 'r') as file:
                parser = ijson.kvitems(file, '')  # Stream key-value pairs from the top-level object
                for username, logs in parser:
                    print(f"{username}: {logs}")
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
        except ijson.JSONDecodeError:
            print(f"Error reading the JSON file '{filename}'.")