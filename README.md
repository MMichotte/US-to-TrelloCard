# US-to-TrelloCard
Python script that enables me to convert à User-Story (with a defined structure) to a Trello card

## Instructions
> instructions for OSX systems

1. Download repository 
2. In the root dir, create a python venv 
    ```bash
    python3 -m venv venv
    ```
3. Install dependencies 
    ```bash
    source venv/bin/activate
    pip3 install -r requirements.txt
    ```
4. Create `.env` file based on the `.envTemplate`
5. Run script :
    ```bash
    python3 src/addTrelloCards.py example/example.md
    ```

❗️ The file structure of your .md file must be similar as the first User-Story of the example.md file : 

- The user-story **must** be contained between the `<!--us-->` abd `<!--/us-->`tags
- The description of the user-story **must** be contained between the `<!--description-->` and `<!--/description-->` tags.
- You can add one or more checklists by containing the items in between the  `<!--checklist: "your checklist name-->` and `<!--checklist-->` tags. Replace `"your checklist nam"` by the name you want to give your checklisr.
- You can add on or more images by enclosing the markdown image syntax (`![desc](path)`) in between the `<!--img-->` and `<!--/img-->` tags. 
  
❗️ The US won't be added if it doesn't have a title and a description.

❗️ Your Trello list **must** have a label named `US`.

🔍 You'll find a code-snippets script in the .vscode folder of this projet. Use it to easily generate a user-story structure in your .md file! 