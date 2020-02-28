import re

import requests

from extractors.result import Result
from extractors.errors import errors, NotFoundException


HEADERS = {
    "accept":
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":
    "gzip, deflate, br",
    "accept-language":
    "zh-CN,zh;q=0.9",
    "cache-control":
    "max-age=0",
    "sec-fetch-mode":
    "navigate",
    "sec-fetch-site":
    "none",
    "upgrade-insecure-requests":
    "1",
    "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

SINGER_PATTERN = r',"nick":"(.*?)",'
SONG_NAME_PATTERN = r'"song_name":"(.*?)",'
PLAY_URL_PATTERN = r'"playurl":"(.*?)",'
PLAY_VIDEO_PATTERN = r',"playurl_video":"(.*?)",'


def get(url:str) -> dict:
    result = Result()
    try:
        with requests.get(url=url, headers=HEADERS, timeout=50) as rep:
            if rep.status_code == 200:
                html = rep.text
                singer = re.findall(SINGER_PATTERN, html)
                if singer:
                    singer = singer[0]
                    result.author = singer
                song_name = re.findall(SONG_NAME_PATTERN, html)
                if song_name:
                    song_name = song_name[0]
                    result.audioName = song_name
                play_url = re.findall(PLAY_URL_PATTERN, html)
                if play_url:
                    result.audioUrls.extend(play_url)
                play_video = re.findall(PLAY_VIDEO_PATTERN, html)
                if play_video:
                    result.videoUrls.extend(play_video)
            else:
                raise NotFoundException
    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()


if __name__ == "__main__":
    data = get(input("url: \n"))
    print(data)