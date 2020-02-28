import re

import requests

from extractors.result import Result
from extractors.errors import errors, NotFoundException, ServerErrorException


headers = {
    "user-agent":
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Referer": "https://m.bilibili.com/",
}

av_number_pattern = r'av([0-9]*)'
cover_pattern = r'<meta property="og:image" content="(http.*?)"/>'
video_pattern = r"video_url: '(.*?)',"



def get(url: str) -> dict:
    result = Result()
    try:
        av = re.findall(av_number_pattern, url)
        if av:
            av = av[0]
        else:
            raise NotFoundException
        url = f'https://www.bilibili.com/video/av{av}'

        rep = requests.get(url, headers=headers, timeout=15)
        if rep.status_code == 200:
            cover_url = re.findall(cover_pattern, rep.text)
            if cover_url:
                if '@' in cover_url[0]:
                    cover_url[0] = cover_url[0][:cover_url[0].index('@')]
                result.imgUrls.extend(cover_url)
            video_url = re.findall(video_pattern, rep.text)
            if video_url:
                result.videoUrls.extend(video_url)

        elif rep.status_code == 404:
            raise NotFoundException
        else:
            raise ServerErrorException
    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()


if __name__ == "__main__":
    print(get(input("av url: ")))
