import re
import requests

from extractors.result import Result
from extractors.errors import errors, NotFoundException


headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}
title_re = r'"title": "(.*?)",'
mp4_720p_mp4_re = r'"mp4_720p_mp4": "(.*?)",'
mp4_hd_mp4_re = r'"mp4_hd_mp4": "(.*?)",'
mp4_ld_mp4_re = r'"mp4_ld_mp4": "(.*?)"'


def get(url: str) -> dict:
    result = Result()
    try:
        rep = requests.get(url, headers=headers, timeout=20)
        if rep.status_code == 200:
            text = rep.text

            title = re.findall(title_re, text)
            if title:
                result.videoName = title[0]

            mp4_720p_mp4 = re.findall(mp4_720p_mp4_re, text)[0]
            if mp4_720p_mp4:
                result.videoUrls.extend(mp4_720p_mp4)

            mp4_hd_mp4 = re.findall(mp4_hd_mp4_re, text)
            if mp4_hd_mp4:
                result.videoUrls.extend(mp4_hd_mp4)

            mp4_ld_mp4 = re.findall(mp4_ld_mp4_re, text)
            if mp4_ld_mp4:
                result.videoUrls.extend(mp4_ld_mp4)
        else:
            raise NotFoundException
    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()


if __name__ == "__main__":
    # url = 'https://m.weibo.cn/5658716867/4474073062821340'
    # url = 'https://weibo.com/3929428825/IuXpilm1p?type=comment'
    url = input('url: ')
    print(get(url))