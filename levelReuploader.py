#######################################
# reuploads 1.9 gdps levels to 2.1
# also does song replacement as arg 2
# enjoy
# by zmx
######################################

import levelDownloader
import levelConverter
import sys
from commonTypes import LevelString, RobDict
import getpass
import robtopCrypto


if __name__ == "__main__":
    print("~ 1.9 Level Reuploader by zmx ~")

    mainID: int = 128
    try:
        mainID = int(sys.argv[1])
    except BaseException:
        print(f"""Usage: {sys.argv[0]} <id> [audio id]""")
        sys.exit()

    # download level first
    levelDownloader.url = "https://absolllute.com/gdps/\
gdapi/downloadGJLevel19.php"
    levelString: LevelString = LevelString(b"")
    levelInfo: RobDict = RobDict({})

    try:
        levelString, levelInfo = levelDownloader.downloadLevel(mainID)
    except BaseException:
        print("invalid level!")
        sys.exit()

    print(f"Downloaded level `{levelInfo['2']}`")

    # check 1.9 acc data
    robtopCrypto.loginURL = "https://absolllute.com/gdps/gdapi\
/accounts/loginGJAccount.php"
    accUsername: str = input("1.9 Username: ")
    password: str = getpass.getpass("User password: ")

    print("Verifying user...")

    playerID: int = -1
    try:
        playerID = robtopCrypto.loginUser(accUsername, password)[1]
    except BaseException:
        print(f"Could not verify user {accUsername}!")
        sys.exit()

    if int(levelInfo["6"]) != playerID:
        print("User did not make level!")
        sys.exit()

    # level uploading
    robtopCrypto.loginURL = "http://www.boomlings.com/database/\
accounts/loginGJAccount.php"
    levelConverter.url = "http://www.boomlings.com/database/\
uploadGJLevel21.php"
    levelConverter.gameVersion = 21

    accUsername = input("2.1 Username: ")
    password = getpass.getpass("User password: ")

    levelInfo["1"] = "0"

    try:
        levelInfo["35"] = sys.argv[2]
    except BaseException:
        pass

    print("Uploading level...")
    try:
        levelID: int = levelConverter.uploadLevel(
            levelString, levelInfo, accUsername=accUsername, password=password,
            unlisted=False)
        print(f"Level reuploaded to id: {levelID}")
    except BaseException:
        print("couldn't reupload level!\n\
this might mean custom song, try using argument 2!")
