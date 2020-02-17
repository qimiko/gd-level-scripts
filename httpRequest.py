from urllib import request, parse
from typing import Any, Dict

def postRequest(url: str, postData: Dict[str, Any]) -> bytes:
	'''
	Requests-free method of posting to url
	'''
	data = parse.urlencode(postData).encode()
	req =  request.Request(url, data=data)
	return request.urlopen(req).read()