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
   
    url = "https://api.trello.com/1/members/me/boards"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}

    r = requests.get(url,params=params)
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

    url = "https://api.trello.com/1/boards/" + board_id + "/lists"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}
 
    allLists = []

    r = requests.get(url,params=params)
    for lists in r.json():
        list_id = ""
        list_name = ""
        for key, value in lists.items():
            if key == "id":
                list_id = value
            elif key == "name":
                list_name = value
        allLists.append({
            'listId': list_id,
            'listName': list_name
        })   

    for li in allLists: 
        if li['listName'] == LIST_NAME:
            print("Found list.")
            return [li['listId'], allLists]
    
    print("Didn't find list.")
    return False

def findUsLabel(board_id):

    url = "https://api.trello.com/1/boards/" + board_id + "/labels"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}

    r = requests.get(url,params=params)
    for label in r.json():
        label_id = ""
        for key, value in label.items():
            if key == "id":
                label_id = value
            if key == "name":
                if value == "US":
                    print("Found label.")
                    return label_id

def findCards(all_lists):
   
    list_of_cards = []

    for li in all_lists:
        list_id = li["listId"]

        url = "https://api.trello.com/1/lists/" + list_id + "/cards"
        params = {'key': API_KEY, 'token': OAUTH_TOKEN}

        r = requests.get(url,params=params)

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

def addImage(cardId,file_path,filePath,desc):
    
    absFilePath = file_path[0:file_path.rfind("/")] + "/" + filePath

    url = "https://api.trello.com/1/cards/" + cardId + "/attachments"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}
    files = {'file': open(absFilePath, 'rb')}

    r = requests.post(url, params=params, files=files)

    imgUrl = r.json()["previews"][-1]["url"]
    new_desc = desc.replace(filePath,imgUrl)

    url = "https://api.trello.com/1/cards/" + cardId
    params = {
        'key': API_KEY,
        'token': OAUTH_TOKEN,
        'desc': new_desc
        }

    r = requests.put(url,params=params)

    return new_desc


def addCards(list_id,list_of_cards,labelId,file_path,new_cards):
    for new_card in new_cards:
        if not any(card[1] == new_card["title"] for card in list_of_cards):
            url = "https://api.trello.com/1/cards"
            params = {
                'key': API_KEY,
                'token': OAUTH_TOKEN,
                'name': new_card["title"],
                'idList': list_id,
                'desc': new_card["description"],
                'idLabels': labelId
                }

            r = requests.post(url,params=params)
            
            cardId = r.json()["id"]

            for CL in new_card["checklists"]:
                url = "https://api.trello.com/1/cards/" + cardId + "/checklists"
                params = {
                    'key': API_KEY,
                    'token': OAUTH_TOKEN,
                    'name': CL["title"]
                    }
                r2 = requests.post(url,params=params)

                checklistId = r2.json()["id"]

                for CL_item in CL["items"]:
                    url = "https://api.trello.com/1/checklists/" + checklistId + "/checkItems"
                    params = {
                        'key': API_KEY,
                        'token': OAUTH_TOKEN,
                        'name': CL_item
                        }
                    r3 = requests.post(url,params=params)
            
            for img in new_card["images"]:
                new_card["description"] = addImage(cardId,file_path,img["path"],new_card["description"])

            print("Added card : " + new_card["title"])


if __name__ == '__main__': 
    file_path = args()
    board_id = findBoard()
    if board_id:
        get_lists = findList(board_id)
        list_id = get_lists[0]
        all_lists = get_lists[1]
        USLabel_id = findUsLabel(board_id)
        if list_id and USLabel_id:
            list_of_cards = findCards(all_lists)
            if list_of_cards:
                new_cards = parseFile(file_path)
                if new_cards:
                    addCards(list_id,list_of_cards,USLabel_id,file_path,new_cards)