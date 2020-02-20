#######################################
# merges two+ levels
# for the creators, i guess
# uploads to (1.9) servers automatically and unlisted
# i don't want to figure out 2.1 format :p
# by zmx
######################################

import sys
import os
from typing import List, Any
import levelDownloader
from levelConverter import uploadLevel
from commonTypes import LevelString, RobDict


def listMerge(list1: List[Any], list2: List[Any]) -> List[Any]:
    """
    Merges two lists, keeping order and removing duplicates between two lists
    (while not removing duplicates in the first)
    from https://stackoverflow.com/a/1319355 lol
    """
    resulting_list: List[Any] = list(list1)
    resulting_list.extend(x for x in list2 if x not in resulting_list)
    return resulting_list


def incrementName(name: str) -> str:
    """
    fun little function, increments level names
    """
    if name[-1].isnumeric() and len(name) > 20:
        newInt: int = int(name[-1]) + 1
        return name[:-1] + str(newInt)
    else:
        return name + " 2"


if __name__ == "__main__":
    print("GD Level Merger by zmx")

    if len(sys.argv) < 2:
        print(f"""Usage: {sys.argv[0]} <id> <id>...
The following environment variables modify execution:
PS - download from 1.9 levels
EXPORT - export, do not upload""")
        sys.exit(os.EX_USAGE)

    levels: List[List[str]] = []
    levelHeader: str = ""
    levelInfo: RobDict = RobDict({})

    if os.getenv("MAIN", "false").lower() == "false":
        levelDownloader.url = "https://absolllute.com/gdps/\
gdapi/downloadGJLevel19.php"
    else:
        print("2.1 level download enabled!")


    for id in sys.argv[1:]:
        try:
            levelString, curLevelInfo = levelDownloader.downloadLevel(
                int(id))  # i promise this isn't dangerous
            print(f"Downloaded level `{curLevelInfo['2']}`")

            levelObjects = levelString.decode().split(';')
            curLevelHeader = levelObjects.pop(0)
            levels.append(levelObjects)

            if sys.argv[1] == id:
                levelInfo = curLevelInfo
                print(f"Using info from `{levelInfo['2']}`")
                levelHeader = curLevelHeader
        except BaseException:
            print("Please specfiy a valid id!")
            sys.exit(os.EX_DATAERR)

    finalLevel = List[List[str]]
    finalLevel = levels[0]

    for pos, objects in enumerate(levels[1:]):
        print(f"Merging level {pos + 2} to level 1")
        finalLevel = listMerge(finalLevel, objects[:-1])
        # last object is ;, keep that outta here

    print(f"Final Object Count: {len(finalLevel)}")

    finalLevelStr: str = levelHeader + ";" + (';').join(finalLevel) + ";"

    levelInfo["2"] = incrementName(levelInfo["2"])

    if os.getenv("EXPORT", "false").lower() == "true":
        print("Exporting level...")
        with open(levelInfo['2'] + '.txt', 'w') as lvlFile:
            lvlFile.write(finalLevelStr)
        sys.exit()

    print("Uploading level...")
    try:
        levelID: int = uploadLevel(LevelString(
            finalLevelStr.encode()), levelInfo)
        print(f"Level reuploaded to id: {levelID}")
    except BaseException:
        print("couldn't reupload level!")
