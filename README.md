# User-Story to Trello-Card

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/MMichotte/US-to-TrelloCard/blob/main/LICENSE) [![PyPi Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)]() ![release](https://img.shields.io/github/v/release/MMichotte/US-to-TrelloCard) ![downloads](https://img.shields.io/github/downloads/MMichotte/US-to-TrelloCard/total.svg)

It has always been a struggle to translate a bunch of well-documented User-Stories written in a markdown or a text file to corresponding Trello cards. 

This project gives you the ability to automate this process just by adding a few `tags`to your User-Stories. 
The tags are nothing more than html comments and are therefor not visible when displayed on github. 

----
## 🏷 Available tags :
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

1. Download and unzip the latest release [here](https://github.com/MMichotte/US-to-TrelloCard/releases) or use `wget`:
   ```bash
   wget https://github.com/$(wget https://github.com/MMichotte/US-to-TrelloCard/releases/latest -O - | egrep '/.*/.*/.*zip' -o)
   ```
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
   ![key&token](example/img/key-token.png)
5. Run script :
    ```bash
    python3 src/add_trello_cards.py -F path/to/your/user-story-file
    ```

## 🔍 Example :
![live example](example/img/live_example.gif)

## 🖌 Snippets : 
To improve your productivity, you can generate a template for your user-story by using the provided code-snippets. 
Feel free to modify the code snippets to your needs but be sure to keep using the correct tags! 

> To start using the snippets, simply copy/paste the content of the `.vscode`folder of this repository into yours. 

![snippets example](example/img/snippets_example.gif)

## 🎯 GitHub Actions :
For even more automation, you can use this script in a `Github Actions` workflow. Give a look at [this file](https://github.com/MMichotte/SLG_APP/blob/master/.github/workflows/Trello.yml) for a real-life example. 

---
### Release strategy :
Each release has it's own tag representing the version of the code at the time of the release. Each tag has the following format : `vX.Y.Z`.

A release is made when :
   - an issue/bug is fixed (`Z` value of the version/tag is incremented)
   - a new feature is added (`Y` value of the version/tag is incremented)
   - major updated (`X` value of the version/tag is incremented)
