import base64
import zlib
import plistlib
import gzip
from typing import Any, Dict, List
from commonTypes import LevelString

# thanks absolute


def Xor(data: Any, key) -> str:
    res = []
    for i in data:
        res.append(i ^ key)
    return bytearray(res).decode()


def decodeRobFile(text: str) -> str:
    decrypted = Xor(str.encode(text), 11)
    decoded = base64.urlsafe_b64decode(decrypted)
    decompressed = zlib.decompress(decoded, 31)
    return decompressed.decode('UTF8')


def encryptRobFile(text: str) -> str:
    compressed = zlib.compress(text.encode())
    encoded = base64.urlsafe_b64encode(compressed)
    encrypted = Xor(encoded, 11)
    return encrypted


def decodeLevel(string: str) -> LevelString:
    try:
        decoded = base64.urlsafe_b64decode(string)
    except BaseException:
        # string is either invalid or already decoded
        if string.startswith("kS"):
            return LevelString(string.encode())
        else:
            raise Exception()
    try:
        decompressed = gzip.decompress(decoded)  # bug on 2.1  idk...?
    except BaseException:
        decompressed = zlib.decompress(decoded, zlib.MAX_WBITS)
        #  1.9 handling except if this errors then :p
    # i also just remembered i have no idea how i found out about this lol
    return LevelString(decompressed)


def encodeLevel(levelString: LevelString) -> bytes:
    return base64.urlsafe_b64encode(zlib.compress(levelString))

# for some reason plistlib doesn't like rob format, wonder why


def shorthandToLong(string: str) -> str:
    newString = string.replace('k>', 'key>')
    newString = newString.replace('d>', 'dict>')
    newString = newString.replace('s>', 'string>')
    newString = newString.replace('r>', 'real>')
    newString = newString.replace('i>', 'integer>')
    newString = newString.replace('<t', '<true')
    newString = newString.replace(' gjver="2.0"', '')
    return newString


def getLevels(string: str) -> List[Dict[str, Any]]:
    if 'k>' in string:
        string = shorthandToLong(string)

    localLevels = plistlib.loads(string.encode())

    levels = localLevels["LLM_01"]
    levels.pop("_isArr")
    levelArray = []

    for lvlid, level in levels.items():
        rev = 1
        try:
            rev = level["k46"]
        except BaseException:
            rev = 1
        try:
            levelString = level["k4"]
        except BaseException:
            levelString = ""
        levelInfo = {"id": lvlid,
                     "name": level["k2"], "string": levelString, "rev": rev}
        levelArray.append(levelInfo)

    return levelArray


def injectLevel(locallevels: str, string: str, id: str) -> str:
    if 'k>' in locallevels:
        locallevels = shorthandToLong(locallevels)

    localLevels = plistlib.loads(locallevels.encode())
    localLevels["LLM_01"][id]["k4"] = string
    return plistlib.dumps(localLevels, sort_keys=False).decode('UTF-8')


if __name__ == "__main__":
    import sys
    import os
    from PyInquirer import prompt  # type: ignore

    with open('CCLocalLevels.dat', 'r') as localLevels:
        decoded = decodeRobFile(localLevels.read())
        gdLevels = getLevels(decoded)

        # get level selection
        levelNames = map(lambda x: x["name"], gdLevels)

        actions = prompt([
            {'type': 'list', 'name': 'action', 'message': 'what do?',
                'choices': ['Import', 'Export']},
            {'type': 'list', 'name': 'level', 'message': 'what level?',
                'choices': levelNames},
            {'type': 'input', 'name': 'filename', 'message': 'what file?'}])
        selectedLevel = filter(
            lambda x: x["name"] == actions["level"], gdLevels)
        # guess who's not subscriptable now!
        selectedLevel = list(selectedLevel)[0]

        # will probably split these into functions at some point but at the
        # same time i don't think that's needed
        if actions["action"] == "Export":
            with open(actions["filename"], 'wb') as levelFile:
                levelFile.write(decodeLevel(selectedLevel['string']))
                print('exported!')
                sys.exit()
        elif actions["action"] == "Import":
            if not os.path.isfile(actions['filename']):
                print('bad file!')
                sys.exit(1)
            with open(actions["filename"], 'r') as levelString:
                with open("CCLocalLevels.dat.new", 'w') as newLocalLevels:
                    newCC = injectLevel(
                        decoded, levelString.read(), selectedLevel['id'])
                    newLocalLevels.write(encryptRobFile(newCC))
                    print('imported level!')
                    sys.exit()
