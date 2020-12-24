# US-to-TrelloCard
Python script that enables me to convert à User-Story (with a defined structure) to a Trello card

## How to Use 
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
    python3 src/addTrelloCard.py example/example.md
    ```

❗️ The file structure of your .md file must be similar as the first User-Story of the example.md file! 
❗️ Your Trello list **must** have a label named `US`.
