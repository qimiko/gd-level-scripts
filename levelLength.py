####################
# Reimplementation of the GDCF method for getting level length
# Values stolen from GDCF and GDBrowser
# (mostly) created by zmx
####################

from typing import Tuple, List, Dict
from enum import Enum
import math
from levelUtil import parseKeyVarArray

# stolen magic values from stadust


class Portals(Enum):
    SLOW = 251.16
    NORMAL = 311.58
    MEDIUM = 387.42
    FAST = 468.0
    SUPER_FAST = 576.0


portalInfo = Tuple[float, Portals]


def getPortalFromId(objectId: int) -> Portals:
    # lol also stolen from stadust
    portalIds: Dict[int,
                    Portals] = {200: Portals.SLOW,
                                201: Portals.NORMAL,
                                202: Portals.MEDIUM,
                                203: Portals.FAST,
                                1334: Portals.SUPER_FAST}

    # script takes care of error handlings
    return portalIds[int(objectId)]


def getPortalInfo(portalIndex: int) -> Portals:
    portalVals: List[Portals] = [
        Portals.NORMAL,
        Portals.SLOW,
        Portals.MEDIUM,
        Portals.FAST,
        Portals.SUPER_FAST]
    try:
        portalInfo = portalVals[portalIndex]
    except BaseException:
        portalInfo = portalVals[0]
    return portalInfo

# x val, portal id


def getPortalList(objects: List[Dict[str, str]]) -> List[portalInfo]:
    portals: List[portalInfo] = []
    for objec in objects:
        try:
            portalId: Portals = getPortalFromId(int(objec['1']))
            if objec['13'] == '1':  # checked portal
                # id, x-pos
                portals.append((float(objec['2']), portalId))
        except BaseException:
            pass
    sPortals: List[portalInfo] = sorted(
        portals, key=lambda x: x[0])  # sort by x pos
    return sPortals

# reimplementation of stadust's function


def getSecondsFromxPos(
        levelLength: float,
        startSpeed: Portals,
        portals: List[portalInfo]) -> float:
    speed: float = startSpeed.value

    if not portals:
        return levelLength / speed

    lastObjPos: float = 0.0
    totalTime: float = 0.0

    for (x, portal) in portals:
        currentSegment: float = x - lastObjPos
        if levelLength <= currentSegment:
            break

        totalTime += currentSegment / speed

        speed = portal.value
        lastObjPos = x

    return (levelLength - lastObjPos) / speed + totalTime


def getLevelLength(levelString: str) -> float:
    """
    - expects a level string lol
    - returns seconds
    """
    # first we want to get the starting portal, i guess
    # this is found in the levle header
    levelObjectsUnp: List[str] = levelString.split(';')
    levelHeader: str = levelObjectsUnp.pop(0)

    # ok next we get value
    dictHeader: Dict[str, str] = parseKeyVarArray(levelHeader, ',')

    levelSpeed: int
    try:
        levelSpeed = int(dictHeader['kA4'])
    except BaseException:
        # does rob just not put it ? no idea but let's not find out
        levelSpeed = 0

    # last object is gross
    levelObjectsUnp.pop()

    levelObjects: List[Dict[str, str]] = list(
        map(lambda x: parseKeyVarArray(x, ','), levelObjectsUnp))
    levelPortals: List[portalInfo] = getPortalList(levelObjects)

    furthestX: float = 0.0
    # probably could be optimized - we iterate over this list a lot
    for objec in levelObjects:
        furthestX = max(furthestX, float(objec['2']))

    seconds: float = getSecondsFromxPos(
        furthestX, getPortalInfo(levelSpeed), levelPortals)
    return seconds


if __name__ == "__main__":
    import sys
    import os
    import levelDownloader

    print("~ Level Length Calculator by zmx (formula from stadust) ~")

    levelFile: str = ''
    levelString: bytes = b''

    if os.getenv("MAIN", "false").lower() == "false":
        levelDownloader.url = "https://absolllute.com/gdps/\
gdapi/downloadGJLevel19.php"

    if len(sys.argv) != 2:
        print(f"""Usage: {sys.argv[0]} <id>...
The following environment variables modify execution:
MAIN - download from 2.1""")
        sys.exit(os.EX_USAGE)

    try:
        levelFile = sys.argv[1]
        levelString, levelInfo = levelDownloader.downloadLevel(int(levelFile))
        print(f'Downloaded level `{levelInfo["2"]}`')
    except BaseException:
        print("could not download level!")
        sys.exit(1)
    seconds = getLevelLength(levelString.decode('utf8'))
    minutes, mSeconds = divmod(seconds, 60.0)
    print(f'Length: {round(minutes)}m {math.ceil(mSeconds)}s')  # accurate to gd?
