import json
import re
class logHandler:

    def extract_card_data(file_path):
        with open(file_path, 'r') as file:
          log_data = file.read()

        
        match = re.search(r'Event_SetDeckV2.*?({.*})', log_data)
        if not match:
            print("No deck data found.")
            return
    
        
        json_data = match.group(1)
    
        
        try:
            deck_data = json.loads(json.loads(json_data)["request"])
            main_deck = deck_data["Deck"].get("MainDeck", [])
            sideboard = deck_data["Deck"].get("Sideboard", [])
        
            
            all_cards = main_deck + sideboard

            arr=[]
            for card in all_cards:
                arr.append([card['cardId'],card['quantity']])
            return(arr)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            
    def saveData():
        print("")
        
        
    log_file_path = "Logs\\UTC_Log_-_12-03-2024_22.17.25.log"
    # extract_card_data(log_file_path)