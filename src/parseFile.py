import sys


def removeLine(d, lineStart):
    doc = d 
    line = doc[lineStart:doc.find("\n",lineStart)]
    doc = doc.replace(line,"")
    return doc

def parseFile(file_path):
    f = file_path

    userStories = []
    newCards = []
    
    with open(f,'r') as file:
        content = file.read()
        file.close()
    
    # extract all User-Stories 
    us_start = content.find("\n",content.find("<!--us-->",0))
    us_stop = content.find("<!--/us-->",us_start)
    while us_start != -1 and us_stop != -1:
        us = content[us_start:us_stop]
        userStories.append(us)
        us_start = content.find("\n",content.find("<!--us-->",us_stop))
        us_stop = content.find("<!--/us-->",us_start)
    
    for us in userStories:
        #get the title
        title_start =  us.find("\n",us.find("<!--title-->"))+1
        title_stop = us.find("<!--/title-->",title_start)
        cardTitle = us[title_start:title_stop].strip("#").strip()

        
        #get the checklists
        checklists = []
        cl_start = us.find("<!--checklist: ",0)
        cl_stop = us.find("<!--/checklist-->",cl_start)
        while cl_start != -1:
            clTitle = us[cl_start:us.find("\n",cl_start)].split("\"")[1]
            clItems = us[us.find("\n",cl_start):cl_stop].splitlines()[1:-1]
            for i in range(len(clItems)):
                clItems[i] = clItems[i].strip(" -*")
            checklists.append(
                {
                    "title": clTitle,
                    "items": clItems
                }
            )
            us = removeLine(us,us.find("<!--checklist: "))
            us = removeLine(us,us.find("<!--/checklist-->"))
            cl_start = us.find("<!--checklist: ",cl_stop)
            cl_stop = us.find("<!--/checklist-->",cl_start)
        
        #get the description
        desc_start =  us.find("\n",us.find("<!--description-->"))+1
        desc_stop = us.find("<!--/description-->",desc_start)
        description = us[desc_start:desc_stop].strip()
        descriptionLines = description.splitlines()
        for l in range(len(descriptionLines)):
            descriptionLines[l] = descriptionLines[l] + "\n"
            if descriptionLines[l].find("#") != -1:
                descriptionLines[l-1] = descriptionLines[l-1] + "\n"
                descriptionLines[l] = descriptionLines[l] + "----\n" + "\n\n --- \n\n"
        
        description = ""
        for l in descriptionLines:
            description += l

        description = description.replace("#","").replace("<u>","").replace("</u>","")
        if cardTitle != "" and description != "":
            newCards.append(
                {
                    "title": cardTitle,
                    "description": description,
                    "checklists": checklists
                }
            )

        
    return newCards



if __name__ == '__main__': 
    parseFile("../example/example.md")