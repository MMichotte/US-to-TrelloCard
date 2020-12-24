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


def readFile(file_path):
    f = file_path
    list_of_new_cards = []
    
    with open(f,'r') as file:
        content = file.read()
        file.close()
    
    us_list = content.split("---")[0:-1]

    for us in us_list:
        try:
        
            checkLists = []

            checkL_start = us.find("<!-- SCHECK ",0)
            while checkL_start != -1:
                checkL_end = us.find("<!-- ECHECK ",checkL_start)
                checkL_info = us[checkL_start:checkL_end].splitlines()
                items = []
                for i in checkL_info[1:]:
                    items.append(i.strip(" - "))

                checkList = {
                    "title": checkL_info[0].replace("<!-- SCHECK : ","").replace(" -->",""),
                    "items": items[:-1]
                }
                checkLists.append(checkList)

                l_start = us[checkL_start:us.find("\n",checkL_start)]                
                l_end = us[checkL_end:us.find("\n",checkL_end)]
                us = us.replace(l_start,"")
                us = us.replace(l_end,"")
                checkL_start = us.find("<!-- SCHECK ",checkL_end + 10)
            
            us = us.replace("<u>","")
            us = us.replace("</u>","")
            p1_start = us.find("### ",0)
            p2_start = us.find("#### ",0)
            p3_start = us.find("#### ",p2_start + 10)
            p4_start = us.find("#### ",p3_start + 10)

            if p1_start ==-1 or p1_start ==-1 or p3_start ==-1 or p4_start ==-1: 
                raise NameError('invalid US') 

            p1_block = us[p1_start:p2_start].splitlines()
            p2_block = us[p2_start:p3_start].strip()
            p3_block = us[p3_start:p4_start].strip()
            p4_block = us[p4_start:].strip()

            us_title =  p1_block[0].lstrip("### ")
            us_explanation = p1_block[1] + "\n\n --- \n\n"
            
            us_preconditions = p2_block.replace("#### ","").replace("\n","\n----\n",1) + "\n\n --- \n\n"
            us_detail = p3_block.replace("#### ","").replace("\n","\n----\n",1) + "\n\n --- \n\n"
            us_validation = p4_block.replace("#### ","").replace("\n","\n----\n",1) 

            us_description = us_explanation + us_preconditions + us_detail + us_validation
            
            #print(us_title)
            #print(us_description)
            
            card = {
                "title": us_title,
                "description": us_description,
                "checklists": checkLists
            }
            
            list_of_new_cards.append(card)
        except Exception as e:
            print(e)
    
    return list_of_new_cards

if __name__ == '__main__': 
    file_path = args()
    board_id = findBoard()
    if board_id:
        list_id = findList(board_id)
        USLabel_id = findUsLabel(board_id)
        if list_id and USLabel_id:
            list_of_cards = findCards(list_id)
            if list_of_cards:
                new_cards = readFile(file_path)
                if new_cards:
                    addCards(list_id,list_of_cards,USLabel_id,new_cards)