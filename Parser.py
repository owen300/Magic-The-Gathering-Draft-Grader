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

        
        match = re.search(r'Event_SetDeckV2.*?({.*})', log_data)#search for this part of the file if it exists
        if not match:
            print("No deck data found.")
            return
    
        
        json_data = match.group(1)#get all the cards and quantitys to a group
    
        
        try:
            deck_data = ijson.loads(ijson.loads(json_data)["request"])
            main_deck = deck_data["Deck"].get("MainDeck", [])#get main deck cards
            sideboard = deck_data["Deck"].get("Sideboard", [])#get side deck cards
        
            
            all_cards = main_deck + sideboard# put it together

            arr=[]
            for card in all_cards:
                arr.append([card['cardId'],card['quantity']])#put the data in an array
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
                json.dump({}, file) 
            print(f"Initialized file '{filename}'.")
        else:
            print(f"File '{filename}' already exists.")

    def add_user_data(self, username=None, data=None):
        if username is None or data is None:# if there is a username or data
            print("Username and data must be provided.")
            return

        # Read existing content incrementally using ijson
        content = {}
        try:
            with open(filename, 'r') as file:#open the userdata json
          
                content = {key: value for key, value in ijson.kvitems(file, '')}
        except (json.JSONDecodeError, FileNotFoundError):
            print("JSON file is empty, corrupted, or does not exist. Initializing a new file.")
            self.initialize_json()#if there is a problem with the json or no json, make one

        if username not in content:
            content[username] = []#if the user doesnt have a section, give them one

        if data in content[username]:
            print(f"Data '{data}' already exists for user '{username}'.")
            return#if the file was already uploaded for the user, do nothing and let them know
        else:
            content[username].append(data)
            print(f"Data '{data}' added for user '{username}'.")
            #put the filename in the users section
        try:
            with open(filename, 'w') as file:
                json.dump(content, file, indent=4)#make the change
            print(f"Data saved successfully for user '{username}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def get_user_logs(self, username=None):
    # Retrieve and return logs for the specified username incrementally using ijson.
        try:
            with open(filename, 'r') as file:
                parser = ijson.kvitems(file, '')
                for user, logs in parser:
                    if user == username:
                        print(f"{user}: {logs}")
                        return logs  # Return logs for the specified username
            print(f"No logs found for username '{username}'.")
            return []
        except FileNotFoundError:
            print(f"The file '{filename}' does not exist.")
            return []
        except ijson.JSONDecodeError:
            print(f"Error reading the JSON file '{filename}'.")
            return []