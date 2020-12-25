from parseFile import *
import sys
import requests
from decouple import config

API_KEY = config("API_KEY")
OAUTH_TOKEN = config("OAUTH_TOKEN")

BOARD_NAME = config("BOARD_NAME")
LIST_NAME = config("LIST_NAME")

AUTH = "?key=" + API_KEY + "&token=" + OAUTH_TOKEN + "&response_type=token"

def args():
    try:
        return sys.argv[1]
    except:
        return False

def findBoard():
   
    get_boards_url = "https://api.trello.com/1/members/me/boards" + AUTH

    r = requests.get(get_boards_url)
    for boards in r.json():
        board_id = ""
        board_name = ""
        for key, value in boards.items():
            #print(str(key) + " : " + str(value))
            if key == "id":
                board_id = value
            elif key == "name":
                board_name = value

        if board_name == BOARD_NAME:
            print("Found board.")
            return board_id
    
    print("Didn't find board.")
    return False

def findList(board_id):
   
    get_lists_url = "https://api.trello.com/1/boards/" + board_id + \
                    "/lists" + AUTH
 
    r = requests.get(get_lists_url)
    for lists in r.json():
        list_id = ""
        list_name = ""
        for key, value in lists.items():
            if key == "id":
                list_id = value
            elif key == "name":
                list_name = value
        if list_name == LIST_NAME:
            print("Found list.")
            return list_id
    
    print("Didn't find list.")
    return False

def findUsLabel(board_id):
    get_lists_url = "https://api.trello.com/1/boards/" + board_id + \
                    "/labels" + AUTH

    r = requests.get(get_lists_url)
    for label in r.json():
        label_id = ""
        for key, value in label.items():
            if key == "id":
                label_id = value
            if key == "name":
                if value == "US":
                    print("Found label.")
                    return label_id

def findCards(list_id):
   
    get_cards_url = "https://api.trello.com/1/lists/" + list_id + \
                    "/cards" + AUTH

    list_of_cards = []

    r = requests.get(get_cards_url)
    for cards in r.json():
        card_id = ""
        card_name = ""
        card_due = ""
        card_desc = ""

        for key, value in cards.items():
            if key == "id":
                card_id = value
            elif key == "name":
                card_name = value
            elif key == "due":
                card_due = value
            elif key == "desc":
                card_desc = value
            list_of_cards.append([card_id, card_name, card_due, card_desc])

    if len(list_of_cards) > 0:
        return list_of_cards
    else:
        return False

def addCards(list_id,list_of_cards,labelId,new_cards):
    for new_card in new_cards:
        if not any(card[1] == new_card["title"] for card in list_of_cards):
            r = requests.post("https://api.trello.com/1/cards" + AUTH + \
                            "&name=" + new_card["title"] + \
                            "&idList=" + list_id + \
                            "&desc=" + new_card["description"] + \
                            "&idLabels=" + labelId)
            
            cardId = r.json()["id"]

            for CL in new_card["checklists"]:
                r2 = requests.post("https://api.trello.com/1/cards/" + cardId + \
                                "/checklists" + AUTH + \
                                "&name=" + CL["title"])

                checklistId = r2.json()["id"]

                for CL_item in CL["items"]:
                    r3 = requests.post("https://api.trello.com/1/checklists/" + checklistId + \
                                    "/checkItems" + AUTH + \
                                    "&name=" + CL_item)
            
            print("Added card : " + new_card["title"])


if __name__ == '__main__': 
    file_path = args()
    board_id = findBoard()
    if board_id:
        list_id = findList(board_id)
        USLabel_id = findUsLabel(board_id)
        if list_id and USLabel_id:
            list_of_cards = findCards(list_id)
            if list_of_cards:
                new_cards = parseFile(file_path)
                if new_cards:
                    addCards(list_id,list_of_cards,USLabel_id,new_cards)