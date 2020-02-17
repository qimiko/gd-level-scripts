from commonTypes import LevelString
import levelUtil, saveUtil, sys, httpRequest
import requests  # type: ignore
from commonTypes import LevelString, RobDict
from typing import Tuple, Dict

gameV = 22
url = 'http://www.boomlings.com/database/downloadGJLevel21.php'
secret = 'Wmfd2893gb7'

def downloadLevel(id: int) -> Tuple[LevelString, RobDict]:
	postdata = {'levelID': id, 'gameVersion': gameV, 'secret': secret}
	downloaded = httpRequest.postRequest(url, postdata)
	levelInfo = levelUtil.parseKeyVarArray(downloaded.decode(), ':')
	levelString = LevelString(saveUtil.decodeLevel(levelInfo['4']))

	return levelString, levelInfo

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawDescriptionHelpFormatter,
			description="Downloads GD Levels", epilog="Daily ID: -1, Weekly ID: -2")

	parser.add_argument('id', help='Level ID (int, required)', type=int)

	parser.add_argument('--gameversion', '-gv',
											help='Game Version (defaults to 22, int)', type=int, default=22)

	parser.add_argument('--url', help='Site URL (defaults to www.boomlings.com)', default='http://www.boomlings.com/database/downloadGJLevel21.php')

	parser.add_argument(
		'--secret', '-s', help='Secret (Don\'t set this unless you know what you\'re doing!, autoset)', default='Wmfd2893gb7')

	args = parser.parse_args()

	# setup values
	gameV = args.gameversion
	url = args.url
	secret = args.secret

	levelString, levelInfo = downloadLevel(args.id)

	if sys.stdout.isatty():
		print(f'Name: {levelInfo["2"]}\nVersion: {levelInfo["13"]}')
		with open(levelInfo['2'] + '.txt', 'wb') as levelFile:
			levelFile.write(levelString)
	else:
		print(levelString.decode('utf-8'))
