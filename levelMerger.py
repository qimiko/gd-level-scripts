#######################################
# merges two+ levels
# for the creators, i guess
# uploads to servers automatically and unlisted
# by zmx
######################################

import sys
import os
from typing import List, Any
import levelDownloader
import levelConverter
from commonTypes import LevelString, RobDict
import saveUtil


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


def getObjCount(levelString: LevelString) -> int:
    """
    Gets object count for a level
    """
    objects = levelString.split(b';')
    return len(objects[1:-1])


if __name__ == "__main__":
    print("~ GD Level Merger by zmx ~")

    if len(sys.argv) < 2:
        print(f"""Usage: {sys.argv[0]} <id> <id>...
The following environment variables modify execution:
MAIN - download from 2.1 levels (and upload to)
EXPORT - export, do not upload""")
        sys.exit()

    levels: List[List[str]] = []
    levelHeader: str = ""
    levelInfo: RobDict = RobDict({})

    if os.getenv("MAIN", "false").lower() == "false":
        levelDownloader.url = "https://absolllute.com/gdps/\
gdapi/downloadGJLevel19.php"
    else:
        print("2.1 level download/upload enabled!")
        levelConverter.url = "http://www.boomlings.com/database/\
uploadGJLevel21.php"
        levelConverter.gameVersion = 21

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
            sys.exit()

    finalLevel = List[List[str]]
    finalLevel = levels[0]

    for pos, objects in enumerate(levels[1:]):
        print(f"Merging level {pos + 2} to level 1")
        finalLevel = listMerge(finalLevel, objects[:-1])
        # last object is ;, keep that outta here

    print(f"Final Object Count: {len(finalLevel)}")

    finalLevelStr: LevelString = LevelString(
        (levelHeader + ";" + (';').join(finalLevel) + ";").encode())
    finalLevelStr = LevelString(saveUtil.encodeLevel(finalLevelStr))

    levelInfo["2"] = incrementName(levelInfo["2"])
    levelInfo["45"] = str(getObjCount(finalLevelStr))

    if os.getenv("EXPORT", "false").lower() == "true":
        print("Exporting level...")
        with open(levelInfo['2'] + '.txt', 'w') as lvlFile:
            lvlFile.write(finalLevelStr)
        sys.exit()

    if levelConverter.gameVersion >= 20:
        import getpass
        accUsername: str = input("Username: ")
        password: str = getpass.getpass("User password: ")
    else:
        accUsername = ""
        password = ""

    print("Uploading level...")
    try:
        levelID: int = levelConverter.uploadLevel(
            finalLevelStr, levelInfo,
            accUsername=accUsername, password=password)
        print(f"Level reuploaded to id: {levelID}")
    except BaseException:
        print("couldn't reupload level!")
