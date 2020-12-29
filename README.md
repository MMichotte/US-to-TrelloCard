# User-Story to Trello-Card

It has always been a struggle to translate a bunch of well-documented User-Stories written in a markdown or a text file to corresponding Trello cards. 

This project gives you the ability to automate this process just by adding a few `tags`to your User-Stories. 
The tags are nothing more than html comments and are therefor not visible when displayed on github. 

----
## 🏷 Available tags:

| Opening tag | Closing tag | Description | Required |
|:-----------:|:-------------:|:-----------:|:--------:|
| `<!--us-->` | `<!--/us-->`    | Delimits a User Story | ✅
| `<!--title-->` | `<!--/title-->` | Delimits the name that will be given to the card, stripped of any `#` character. | ✅
| `<!--description-->` | `<!--/description-->` | Delimits the text that will appear in the cards description. | ✅
| `<!--checklist: "your checklist name"-->` | `<!--checklist-->` | Delimits the items that should be added to a checklist. The checklist will be created with as title the name you pass in between the `"`characters in the opening tag. |
| `<!--img-->` | `<!--/img-->` | Delimits an image inserted in your .md file that should be uploaded as attachment to the card and included in the description. | 

❗️ The user-story won't be added if your US doesn't have the required tags.

## 🚀 Usage : 
⚠️ The following commands are written for `Unix` systems (Linux/OSX). If you're on a windows machine, please give a look at the python documentation to find the corresponding commands. 

1. Download or clone this repository 
2. In the `root` dir, create a `python virtual environment  ` (*Optional but recommended*)
    ```bash
    python3 -m venv venv #creating virtual env
    source venv/bin/activate #activating the created venv
    ```
3. Install required dependencies 
    ```bash
    pip3 install --upgrade pip #updating your pip version
    pip3 install -r requirements.txt #installing dependencies
    ```
4. Rename `.envTemplate` to `.env`and update it with your own information.
   > You can generate your own `api-key` and `oath-token` here : https://trello.com/app-key
5. Run script :
    ```bash
    python3 src/addTrelloCards.py path/to/your/user-story-file
    ```

## 🔍 Examples :
//TODO

## 🖌 Snippets : 

To improve your productivity, you can generate a template for your user-story by using the provided code-snippets. 

Feel free to modify the code snippets to your needs but be sure to keep using the correct tags! 

> To start using the snippets, simply copy/paste the content of the `.vscode`folder of this repository into yours. 
