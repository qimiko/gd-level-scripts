#######################################
# 2.1 level format to 1.9 level auto converter
# for the truest dashers
# uploads to servers automatically and unlisted
# by zmx
######################################

from argparse import ArgumentError
import objCharts
import re
import levelUtil
import levelDownloader
import saveUtil
import sys
import base64
import httpRequest
import os  # for error codes
from typing import Dict
from commonTypes import LevelString, RobDict
import robtopCrypto


url: str = "https://absolllute.com/gdps/gdapi/uploadGJLevel19.php"
gameVersion: int = 19
username: str = "21Reupload"


def uploadLevel(levelString: LevelString, levelInfo: RobDict,
                originalID: int = None, accUsername: str = username,
                password: str = None, unlisted: bool = True) -> int:
    """
    Uploads a level to 1.9 servers
    """

    # 1.9 descriptions aren't base64 encoded, we need to remove illegal
    # characters before upload breaks them anyways
    desc: str = levelInfo["3"]
    if (gameVersion < 20):
        desc = base64.urlsafe_b64decode(desc).decode()
        desc = re.sub(r"[^A-Za-z0-9\., \$\-\_\.\+\!\*\'()]",
                      "", desc)  # remove anything not url safe

    # some params don't exist
    postdata = {
        "gjp": '',
        "gameVersion": gameVersion,
        "binaryVersion": gameVersion + 14,  # definitely not the correct way
        "udid": "S-hi-people",
        "uuid": 3109282,
        "userName": accUsername,
        "unlisted": unlisted,
        "levelDesc": desc,
        "levelName": levelInfo["2"],
        "levelVersion": levelInfo["5"],
        "levelLength": levelInfo["15"],
        "audioTrack": levelInfo["12"],
        "password": 1,
        "levelID": 0,
        "original": levelInfo["1"],
        "songID": levelInfo.get(
            "35",
            0),
        "objects": levelInfo.get(
            "45",
            0),
        "seed2": base64.urlsafe_b64encode(
            robtopCrypto.makeSeed(levelString).encode()),
        "wt2": 0,
        "wt": 3,
        "seed": "PJsBAJ24Po",
        "extraString": ('_'.join(map(str, (0 for _ in range(55))))),
        "levelInfo": saveUtil.encodeLevel(LevelString(b"0;1;1.12;;422.00;;")),
        # thank nekit
        "auto": levelInfo.get("25", 0),
        "twoPlayer": 0,  # going to guess
        "ldm": levelInfo.get("40", 0),
        "coins": levelInfo.get("37", 0),
        "requestedStars": levelInfo.get("39", 0),
        "gdw": 0,
        "secret": "Wmfd2893gb7"}
    postdata["levelString"] = levelString

    if gameVersion >= 20:
        if not password or not accUsername:
            raise ArgumentError(None, "invalid credentials!")
        try:
            accID: int = robtopCrypto.loginUser(accUsername, password)[0]
        except BaseException:
            print("invalid login")
            raise Exception()
        postdata["gjp"] = robtopCrypto.getGJP(password)
        postdata["accountID"] = accID
        postdata["userName"] = robtopCrypto.getUsername(accID)

    uploadRequest = httpRequest.postRequest(url, postdata)

    try:
        levelID: int = int(uploadRequest)
        if levelID == -1:  # -1 is an error dumb
            raise Exception()
        return levelID
    except BaseException:
        print(f"Error occured while reuploading:\n{uploadRequest}")
        raise Exception()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog="1.9 Level Reuploader Tool", description="by zmx")

    parser.add_argument("id", help="id to reupload")
    parser.add_argument(
        "-d", "--dry", help="skip uploading level", action="store_true")
    parser.add_argument(
        "--club", help="convert unlined clubstep blocks 1-8 to those with lines", action="store_true")
    parser.add_argument(
        "--glow", help="convert full glow blocks to 1.9 equivalents", action="store_true")
    parser.add_argument(
        "--color", help="convert colored blocks to non colored 1.9 equivalents", action="store_true")
    parser.add_argument(
        "--song", help="set custom song id", type=int)

    args = parser.parse_args()

    mainID = args.id

    levelString: LevelString = LevelString(b"")
    levelInfo: RobDict = RobDict({})

    try:
        levelString, levelInfo = levelDownloader.downloadLevel(mainID)
    except BaseException:
        print("invalid level!")
        sys.exit()

    print(f"Downloaded level `{levelInfo['2']}`")
    if args.club:
        print("""Clubstep block conversion enabled!
This can make some levels impossible!""")
        levelUtil.convClubstep = True
    if args.color:
        print("""Color block conversion enabled!
This can make some levels impossible!""")
        levelUtil.convColor = True
    if args.glow:
        print("Glow conversion enabled!")
        levelUtil.convGlow = True

    print("Converting...\n")

    # rob likes his levels encoded
    convLevel: LevelString = levelUtil.convLevelString(levelString)
    encodedLevel: bytes = saveUtil.encodeLevel(convLevel)

    illegalObjs: Dict[int, str] = levelUtil.illegalObjInfo(
        levelUtil.illegalObj)

    for objID, name in illegalObjs.items():
        print(f"Illegal object: {objID} ({name})")

    if set(levelUtil.illegalObj).intersection(objCharts.clubstepObjConv):
        print("Note: Enabling the CLUB option will convert",
              "most of the clubstep blocks,",
              "but can make the level impossible!")
    if set(levelUtil.illegalObj).intersection(objCharts.glowObj):
        print("Note: Enabling the GLOW option will convert",
              "most of the full glow blocks!")
    if set(levelUtil.illegalObj).intersection(objCharts.colorDefaultBlockObj):
        print("Note: Enabling the COLOR option will convert",
              "most of the color blocks",
              "but can make the level impossible!")

    if not illegalObjs:
        print("All objects converted!")

    print("")

    if args.song:
        print(f"Setting song to id {args.song} from id {levelInfo['35']}")
        levelInfo['35'] = args.song

    if args.dry:
        print("Dry mode enabled, no upload!")
        sys.exit()

    print("Uploading level...")
    try:
        levelID = uploadLevel(LevelString(encodedLevel), levelInfo)
        print(f"Level reuploaded to id: {levelID}")
    except BaseException:
        print("couldn't reupload level!")
