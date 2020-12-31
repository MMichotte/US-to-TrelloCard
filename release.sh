#!/bin/bash

#This script doesn't release anything, but is used in combination with a github action workflow to create a new release!

GITHUB_USER="MMICHOTTE"
GITHUB_REPO="US-to-TrelloCard"

TYPE=""

read -p $'\nIs this release a \e[34mbug fix (b)\e[0m or a \e[32mnew feature (f)\e[0m? (b/f) ' choice
case "$choice" in 
  b|B ) TYPE="B";;
  f|F ) TYPE="F";;
  * ) echo "invalid" && exit;;
esac

CUR_VERSION=$(curl -s "https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' )
CUR_V_NUM=$(echo $CUR_VERSION | tr -d "v")
NEW_VERSION="v"
COUNT=0
for i in $(echo $CUR_V_NUM | tr "." "\n")
do  
    if [[ $COUNT -eq 0 ]] 
    then
        if [[ $TYPE = "F" ]] 
        then 
            i=$(($i+1))
        fi
        NEW_VERSION+=$i
        NEW_VERSION+="."
    else
        if [[ $TYPE = "F" ]] 
        then 
            i=0 
        else  
            i=$(($i+1))         
        fi
        NEW_VERSION+=$i
    fi    
    COUNT+=1
done

read -p $'Going from version : \e[31m'"${CUR_VERSION}"$' (latest)\e[0m to ----> \e[33m'"${NEW_VERSION}"$'\e[0m OK ? (y/n) ' choice
case "$choice" in 
  y|Y ) echo "";;
  n|N ) exit;;
  * ) echo "invalid" && exit;;
esac

git commit -am "${NEW_VERSION}"
git tag $NEW_VERSION
git push && git push --tags
