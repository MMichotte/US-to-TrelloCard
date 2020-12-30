"""
@Author: Martin Michotte
@Date: 30/12/2020

Multiple functions to add cards to a Trello board using the Trello API.
"""

import sys
import requests
from decouple import config
from parse_file import parse_file

# env variables
API_KEY = config("API_KEY")
OAUTH_TOKEN = config("OAUTH_TOKEN")
BOARD_NAME = config("BOARD_NAME")
LIST_NAME = config("LIST_NAME")
LABELS = config("LABELS").lstrip("[").rstrip("]").split(', ')

# constant variables
BASE_URL = "https://api.trello.com/1/"

def get_args():
    """
    Function that retrieves the script's arguments when executed.

        Parameters:
            /

        Returns:
            A dict containing the various arguments.
    """
    valid_args = {
        "file_path": ""
    }

    args = sys.argv
    for arg_i in range(len(args)):
        if args[arg_i] == "-F" or args[arg_i] == "--file":
            valid_args["file_path"] = args[arg_i + 1]

    if valid_args["file_path"] != "":
        return valid_args

    print("\n\t❌ \033[41mMissing argument : -F or --file \033[0m\n")
    quit()


def find_board():
    """
    Function that finds all the boards of the current user and returns the
    id of the selected board.

    The current user is defined by the API_KEY setting in the .env file.
    The selected board is defined by the BOARD_NAME setting in the .env file.

    If the selected board isn't found, the script execution is stopped.

        Parameters:
            /

        Returns:
            board_id (str): the id of the selected board
    """
    url = BASE_URL + "members/me/boards"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}

    resp = requests.get(url, params=params)
    if resp.status_code == 401:
        print("\n\t❌ \033[41mWrong credentials !\033[0m\n")
        quit()

    for boards in resp.json():
        board_id = ""
        board_name = ""
        for key, value in boards.items():
            # print(str(key) + " : " + str(value))
            if key == "id":
                board_id = value
            elif key == "name":
                board_name = value

        if board_name == BOARD_NAME:
            print("\t✅ Found board: \033[34m" + BOARD_NAME + "\033[0m")
            return board_id

    print("\t❌ Board not found ! --> \033[31m" + BOARD_NAME + "\033[0m\n")
    exit()


def find_list(board_id):
    """
    Function that finds all the lists for a given board returns
    the id of the selected list as well as an array of all lists

    The selected list is defined by the LIST_NAME setting in the .env file.

    If the selected list isn't found, the script execution is stopped.

        Parameters:
            board_id (str): the id of a board

        Returns:
            [
                listId (str): the id of the selected list,
                all_lists ([]): Array of all lists as a dicts:
                    {
                        listId (str): id of the list
                        listName (str): name of the list
                    }
            ]
    """
    url = BASE_URL + "boards/" + board_id + "/lists"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}

    all_lists = []

    resp = requests.get(url, params=params)
    for lists in resp.json():
        list_id = ""
        list_name = ""
        for key, value in lists.items():
            if key == "id":
                list_id = value
            elif key == "name":
                list_name = value
        all_lists.append({
            'listId': list_id,
            'listName': list_name
        })

    for lis in all_lists:
        if lis['listName'] == LIST_NAME:
            print("\t✅ Found List: \033[34m" + LIST_NAME + "\033[0m")
            return [lis['listId'], all_lists]

    print("\t❌ List not found ! --> \033[31m" + LIST_NAME + "\033[0m\n")
    exit()


def find_us_label(board_id):
    """
    Function that finds all the lables for a given board and returns
    the id of the first one that is selected.

    The selected label is defined by the LABLES setting in the .env file.

    If the selected label isn't found, the script execution is stopped.

        Parameters:
            board_id (str): the id of a board

        Returns:
            label_id (str): id of the selected label
    """
    url = BASE_URL + "boards/" + board_id + "/labels"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}

    resp = requests.get(url, params=params)
    for label in resp.json():
        label_id = ""
        for key, value in label.items():
            if key == "id":
                label_id = value
            if key == "name":
                if value == LABELS[0]:
                    print("\t✅ Found Label: \033[34m" + LABELS[0] + "\033[0m")
                    return label_id

    print("\t❌ Label not found ! --> \033[31m" + LABELS[0] + "\033[0m\n")
    exit()


def find_cards(all_lists):
    """
    Function that retrieves all the cards for an array of lists and returns
    an array containing all the cards.

    If zero cards were found, the script execution is stopped.

        Parameters:
            all_lists ([]): array of lists (see find_list()).

        Returns:
            list_of_cards ([]): array of cards.
    """
    list_of_cards = []

    for lis in all_lists:
        list_id = lis["listId"]

        url = BASE_URL + "lists/" + list_id + "/cards"
        params = {'key': API_KEY, 'token': OAUTH_TOKEN}

        resp = requests.get(url, params=params)

        for cards in resp.json():
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
        print("\t❌ No cards found ! --> \033[31mThere must be at least ONE card in any list of your board\033[0m\n")
        exit()


def add_image(card_id, file_path, im_path, desc):
    """
    Function that uploads an image as an attachement to a given card and
    changes the corresponding paths in it's description.

        Parameters:
            card_id (str): id of a card
            file_path (str): the path of the current file that is being processed
            im_path (str): the path of the image
            desc (str): the current description of the card

        Returns:
            new_desc (str): the input description with the new image paths
    """
    abs_file_path = file_path[0:file_path.rfind("/")] + "/" + im_path

    url = BASE_URL + "cards/" + card_id + "/attachments"
    params = {'key': API_KEY, 'token': OAUTH_TOKEN}
    files = {'file': open(abs_file_path, 'rb')}

    resp = requests.post(url, params=params, files=files)

    img_url = resp.json()["previews"][-1]["url"]
    new_desc = desc.replace(im_path, img_url)

    url = BASE_URL + "cards/" + card_id
    params = {
        'key': API_KEY,
        'token': OAUTH_TOKEN,
        'desc': new_desc
        }

    resp = requests.put(url, params=params)

    return new_desc


def add_cards(list_id, list_of_cards, label_id, file_path, new_cards):
    """
    Function that creates a new card in Trello.

        Parameters:
            list_id (str): id of a list
            list_of_cards ([]): array of existing cards in your Trello board
            labelId (str): id of the label to add to the card
            file_path (str): the path of the current file that is being processed
            new_cards ([]): array of all cards that should be processed

        Returns:
            /
    """
    cards_added = 0
    for new_card in new_cards:
        if not any(card[1] == new_card["title"] for card in list_of_cards):
            url = BASE_URL + "cards"
            params = {
                'key': API_KEY,
                'token': OAUTH_TOKEN,
                'name': new_card["title"],
                'idList': list_id,
                'desc': new_card["description"],
                'idLabels': label_id
                }

            resp = requests.post(url, params=params)

            card_id = resp.json()["id"]

            for CL in new_card["checklists"]:
                url = BASE_URL + "cards/" + card_id + "/checklists"
                params = {
                    'key': API_KEY,
                    'token': OAUTH_TOKEN,
                    'name': CL["title"]
                    }
                resp2 = requests.post(url, params=params)

                checklist_id = resp2.json()["id"]

                for CL_item in CL["items"]:
                    url = BASE_URL + "checklists/" + checklist_id + "/checkItems"
                    params = {
                        'key': API_KEY,
                        'token': OAUTH_TOKEN,
                        'name': CL_item
                        }
                    resp3 = requests.post(url, params=params)

            for img in new_card["images"]:
                new_card["description"] = add_image(card_id, file_path, img["path"], new_card["description"])

            cards_added += 1

            print("\t🎯 Added card : \033[32m" + new_card["title"] + "\033[0m")

    if cards_added == 0:
        print("\t💡\033[33mNo cards were added.\033[0m")
    elif cards_added != len(new_cards):
        print("\n\t💡\033[33mSome cards were not added since they already existed.\033[0m")


if __name__ == '__main__':
    print("\n🚀 \033[32mRunning script \033[0m")

    _file_path = get_args()["file_path"]
    _board_id = find_board()
    _get_lists = find_list(_board_id)
    _list_id = _get_lists[0]
    _all_lists = _get_lists[1]
    _US_label_id = find_us_label(_board_id)
    _list_of_cards = find_cards(_all_lists)
    _new_cards = parse_file(_file_path)

    add_cards(_list_id, _list_of_cards, _US_label_id, _file_path, _new_cards)

    print("🎉 \033[32mDone! \033[0m\n")
