from urllib.parse import urlparse

import requests as rs

from extractors.result import Result
from extractors.errors import errors, NotFoundException, ServerErrorException, SpecialErrorException


headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"}
info_url = "https://m.lizhi.fm/vodapi/voice/info/{id}"


def get(url: str) -> dict:
    result = Result()
    try:
        path = urlparse(url).path
        voiceId = path.split("/")[-1]
        if not voiceId:
            raise NotFoundException
        rep = rs.get(info_url.format(id=voiceId), headers=headers, timeout=11)
        if rep.status_code == 200:
            info = rep.json()
            if info['code'] == 0:
                userName = info.get("data").get("userVoice").get("userInfo").get("name")
                voiceName = info.get("data").get("userVoice").get("voiceInfo").get("name")
                voiceUrl= info.get("data").get("userVoice").get("voicePlayProperty").get("trackUrl")
                result.author = userName
                result.audioName = voiceName
                result.audioUrls.append(voiceUrl)
            else:
                raise SpecialErrorException
        else:
            raise NotFoundException
    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()

if __name__ == "__main__":
    url = input("url: ")
    print(get(url))