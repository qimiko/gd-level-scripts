import saveUtil
import hashlib
import base64
from typing import Any, Dict, Tuple
import httpRequest
import levelUtil


def makeSeed(encoded: bytes) -> str:
    """
    seed2 function for robtop games
    """
    seed2: str = ""
    if len(encoded) < 49:
        seed2 = encoded.decode()
    else:
        seed2 = ""
        slot = len(encoded) // 50
        for i in range(0, 50):
            seed2 += encoded.decode()[slot * i]
    return saveUtil.Xor(
        hashlib.sha1(
            seed2.encode() +
            b"xI25fpAapCQg").hexdigest(),
        41274)


def getGJP(password: str) -> bytes:
    """
    gets gjp from password
    """
    return base64.urlsafe_b64encode(saveUtil.Xor(password, 37526).encode())


loginURL: str = "http://www.boomlings.com/database/accounts/loginGJAccount.php"


def loginUser(username: str, password: str) -> Tuple[int, int]:
    """
    logins a user
    returns [account id, player id]
    """
    data: Dict[str, Any] = {
        "userName": username,
        "password": password,
        "secret": "Wmfv3899gc9",
        "udid": "s12-03912-0391-2039"
    }
    loginRequest: bytes = httpRequest.postRequest(loginURL, data)
    if loginRequest == b"-1":
        raise ValueError()

    accID: int = int(loginRequest.split(b',')[0])
    playerID: int = int(loginRequest.split(b',')[1])

    return accID, playerID


userInfoURL: str = "http://www.boomlings.com/database/getGJUserInfo20.php"


def getUsername(accID: int) -> str:
    """
    gets user from account id
    """
    data: Dict[str, Any] = {
        "targetAccountID": accID,
        "secret": "Wmfd2893gb7",
        "gameVersion": 21
    }
    userRequest: bytes = httpRequest.postRequest(userInfoURL, data)
    userInfo = levelUtil.parseKeyVarArray(userRequest.decode(), ":")

    return userInfo["1"]
