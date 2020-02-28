import re

import requests

from extractors.result import Result
from extractors.errors import errors, NotFoundException, ServerErrorException


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

audio_url_pattern = r'<audio src="(http://cdn.singroom.i52hz.com/.*?)" preload="metadata"'
author_pattern = r'"nickname":"(.*?)",'
audio_name_pattern = r'"songName":"(.*?)",'


def get(url: str) -> dict:
    result = Result()
    try:
        rep = requests.get(url, headers=headers, timeout=10)
        if rep.status_code == 200:
            html = rep.text
            author = re.findall(author_pattern, html)
            if author:
                result.author = author[0]
            audio_name = re.findall(audio_name_pattern, html)
            if audio_name:
                result.audioName = audio_name[0]
            audio_url = re.findall(audio_url_pattern, html)
            if audio_url:
                result.audioUrls.extend(audio_url)
            else:
                result.err = 1

        elif rep.status_code == 404:
            raise NotFoundException
        else:
            raise ServerErrorException
    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()

if __name__ == "__main__":
    data = get(input("url: "))
    print(data)
