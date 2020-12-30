"""
@Author: Martin Michotte
@Date: 30/12/2020

Multiple functions to parse a given file.
"""

def remove_line(doc, line_start):
    """
    Removes an entire line from a string starting at a charcater position.

        Parameters:
            doc (str): A string composed of multiple lines.
            line_start (int): Position of the first character of the line to remove in the given string.

        Returns:
            new_doc (str): The new string
    """
    new_doc = doc
    line = new_doc[line_start:new_doc.find("\n",line_start)]
    new_doc = new_doc.replace(line,"")
    return new_doc

def parse_file(file_path):
    """
    Parses a file into different User-Stories.

        Parameters:
            file_path (str): The path to the file that you want to parse.

        Returns:
            new_cards ([]): Array containing all the new cards.

    """
    user_stories = []
    new_cards = []

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            file.close()
        print("\t✅ Found file: \033[34m" + file_path + "\033[0m\n")

    except Exception as err:
        print("\t❌ File not found ! --> \033[31m" + file_path + "\033[0m\n")
        exit()

    # extract all User-Stories
    us_start = content.find("\n", content.find("<!--us-->", 0))
    us_stop = content.find("<!--/us-->", us_start)
    while us_start != -1 and us_stop != -1:
        us = content[us_start:us_stop]
        user_stories.append(us)
        us_start = content.find("\n", content.find("<!--us-->", us_stop))
        us_stop = content.find("<!--/us-->", us_start)

    for us in user_stories:
        #get the title
        title_start =  us.find("\n", us.find("<!--title-->"))+1
        title_stop = us.find("<!--/title-->", title_start)
        card_title = us[title_start:title_stop].strip("#").strip()


        #get the checklists
        checklists = []
        cl_start = us.find("<!--checklist: ",0)
        cl_stop = us.find("<!--/checklist-->",cl_start)
        while cl_start != -1:
            cl_title = us[cl_start:us.find("\n", cl_start)].split("\"")[1]
            cl_items = us[us.find("\n", cl_start):cl_stop].splitlines()[1:-1]

            for i in range(len(cl_items)):
                cl_items[i] = cl_items[i].strip(" -*")
            checklists.append(
                {
                    "title": cl_title,
                    "items": cl_items
                }
            )
            us = remove_line(us, us.find("<!--checklist: "))
            us = remove_line(us, us.find("<!--/checklist-->"))
            cl_start = us.find("<!--checklist: ", cl_stop)
            cl_stop = us.find("<!--/checklist-->", cl_start)

        #get the images
        images = []
        img_start = us.find("<!--img-->", 0)
        img_stop = us.find("<!--/img-->", img_start)
        while img_start != -1:
            img_title = us[us.find("[", img_start):us.find("]", img_start)].lstrip("[")
            img_path = us[us.find("(", img_start):us.find(")", img_start)].lstrip("(")
            images.append(
                {
                    "title": img_title,
                    "path": img_path
                }
            )
            img_start = us.find("<!--img-->",img_stop)
            img_stop = us.find("<!--/img-->",img_start)

        us = us.replace("<!--img-->","")
        us = us.replace("<!--/img-->","")

        #get the description
        desc_start =  us.find("\n", us.find("<!--description-->"))+1
        desc_stop = us.find("<!--/description-->", desc_start)
        description = us[desc_start:desc_stop].strip()
        description_lines = description.splitlines()
        for line in range(len(description_lines)):
            description_lines[line] = description_lines[line] + "\n"
            if description_lines[line].find("#") != -1:
                description_lines[line-1] = description_lines[line-1] + "\n"
                description_lines[line] = description_lines[line] + "----\n" + "\n\n --- \n\n"

        description = ""
        for line in description_lines:
            description += line

        description = description.replace("#", "").replace("<u>", "").replace("</u>", "")
        if card_title != "" and description != "":
            new_cards.append(
                {
                    "title": card_title,
                    "description": description,
                    "checklists": checklists,
                    "images": images
                }
            )


    return new_cards

if __name__ == '__main__':
    parse_file("../example/example.md")
