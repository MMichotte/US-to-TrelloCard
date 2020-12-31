#!/bin/bash

#### README
# This script doesn't release anything, but is used in combination with the following 'Github Action' Workflow
# to create a new release! ( Workflow: https://github.com/actions/upload-release-asset )
# 
# This script does the following: 
#   1. Retrieves the latest tag from your github release page
#   2. Prompts you what type of release you want to do
#   3. Creates a new tag according to your choice
#   4. Commits & pushes your new version and tag (this will be catched by the Github Action Workflow)
#
# The current version/tag format is "v*.*.*" but this can easily be modified to any format!
# Version format: vx.y.z
#   x : Major change -> usaly means big code refactoring or complete remodeling of app 
#   y : Minar change -> added a small new feature or slightly changed UI, ...
#   z : Patch        -> bug fix 
#
###

GITHUB_USER="MMichotte"
GITHUB_REPO="US-to-TrelloCard"
PACKAGE_JSON=false  #set to true if you want the version of you'r package.json file to be changed 

TYPE=""

read -p $'\nIs this release \e[31mMAJOR (m)\e[0m, \e[33mMINOR (s)\e[0m or a \e[32mPATCH (p)\e[0m ? (m/s/p) ' choice
case "$choice" in 
  m|M ) TYPE="M";;
  s|S ) TYPE="S";;
  p|P ) TYPE="P";;
  * ) echo "invalid" && exit;;
esac

CUR_VERSION=$(curl -s "https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' )
CUR_V_NUM=$(echo $CUR_VERSION | tr -d "v")
NEW_VERSION="v"
COUNT=0
for i in $(echo $CUR_V_NUM | tr "." "\n")
do  

    COUNT=$(($COUNT+1))  
    if [[ $COUNT -eq 1 ]] 
    then
        # first digit
        if [[ $TYPE = "M" ]] 
        then 
            i=$(($i+1))
            NEW_VERSION+=$i
            NEW_VERSION+=".0.0"
            break
        fi
        NEW_VERSION+=$i
        NEW_VERSION+="."
    elif [[ $COUNT -eq 2 ]] 
    then 
        # second digit
        if [[ $TYPE = "S" ]] 
        then
            i=$(($i+1))
            NEW_VERSION+=$i
            NEW_VERSION+=".0"   
            break              
        fi
        NEW_VERSION+=$i
        NEW_VERSION+="." 
    else 
        # third (and last) digit
        i=$(($i+1))
        NEW_VERSION+=$i
    fi  
done

case $COUNT in 
  0 ) NEW_VERSION+="0.0.1";;
  1 ) NEW_VERSION+="0.1";;
  2 ) NEW_VERSION+="1";;
  3 ) ;;
  * ) exit;;
esac


read -p $'Going from version : \e[31m'"${CUR_VERSION}"$' (latest)\e[0m to ----> \e[33m'"${NEW_VERSION}"$'\e[0m OK ? (y/n) ' choice
case "$choice" in 
  y|Y ) echo "";;
  n|N ) exit;;
  * ) echo "invalid" && exit;;
esac

if [ "$PACKAGE_JSON" = true ]
then
    VER_LINE=$(awk '/"version":/{ print NR; exit }' ./package.json)
    sed -i '' "${VER_LINE}s/.*/    \"version\": \"${NEW_VERSION}\",/" package.json
fi

git commit -am "${NEW_VERSION}"
git tag $NEW_VERSION
git push && git push --tags
