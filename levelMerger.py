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


def listMerge(list1: List[Any], list2: List[Any], remove_duplicate = True) -> List[Any]:
    """
    Merges two lists, keeping order and removing duplicates between two lists
    (while not removing duplicates in the first)
    from https://stackoverflow.com/a/1319355 lol
    """
    resulting_list: List[Any] = list(list1)

    if remove_duplicate:
        resulting_list.extend(x for x in list2 if x not in resulting_list)
    else:
        resulting_list.extend(x for x in list2)

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
    import argparse

    parser = argparse.ArgumentParser(
        description="GD Level Merger", epilog="hi ~zmx")

    parser.add_argument("base", help="base level", type=int)
    parser.add_argument("ids", help="ids to merge", nargs="+", type=int)
    parser.add_argument(
        "--main", help="use 2.1 servers for download and upload", action="store_true")
    parser.add_argument(
        "--export", help="export level to file, skip upload", action="store_true")
    parser.add_argument(
        "--allow-collisions", help="keep collisions while merging", action="store_true")

    args = parser.parse_args()

    levels: List[List[str]] = []
    levelHeader: str = ""
    levelInfo: RobDict = RobDict({})

    if not args.main:
        levelDownloader.url = "https://absolllute.com/gdps/\
gdapi/downloadGJLevel19.php"
    else:
        print("2.1 level download/upload enabled!")
        levelConverter.url = "http://www.boomlings.com/database/\
uploadGJLevel21.php"
        levelConverter.gameVersion = 21

    # we ensure that at least two arguments are provided
    full_list = [args.base] + args.ids

    for id in full_list:
        try:
            levelString, curLevelInfo = levelDownloader.downloadLevel(
                int(id))  # i promise this isn't dangerous
            print(f"Downloaded level `{curLevelInfo['2']}`")

            levelObjects = levelString.decode().split(';')
            curLevelHeader = levelObjects.pop(0)
            levels.append(levelObjects)

            if id == args.base:
                levelInfo = curLevelInfo
                print(f"Using info from `{levelInfo['2']}`")
                levelHeader = curLevelHeader
        except:
            print(f"Please specfiy a valid id - {id} is broken!")
            sys.exit()

    finalLevel = List[List[str]]
    finalLevel = levels[0]

    allow_collisions = False
    if args.allow_collisions:
        print("collisions enabled!")
        allow_collisions = True

    for pos, objects in enumerate(levels[1:]):
        print(f"Merging level {pos + 2} to level 1")
        if args.allow_collisions:
            finalLevel = listMerge(finalLevel, objects[:-1], not allow_collisions)
        # last object is ;, keep that outta here

    print(f"Final Object Count: {len(finalLevel)}")

    finalLevelStr: LevelString = LevelString(
        (levelHeader + ";" + (';').join(finalLevel) + ";").encode())
    finalLevelStr = LevelString(saveUtil.encodeLevel(finalLevelStr))

    levelInfo["2"] = incrementName(levelInfo["2"])
    levelInfo["45"] = str(getObjCount(finalLevelStr))

    if args.export:
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
