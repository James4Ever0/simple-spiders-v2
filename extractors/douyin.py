import re

import requests

from extractors.result import Result
from extractors.errors import errors, NotFoundException, ServerErrorException


headers = {
    'accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':
    'gzip, deflate, br',
    'accept-language':
    'zh-CN,zh;q=0.9',
    'cache-control':
    'max-age=0',
    'upgrade-insecure-requests':
    '1',
    'user-agent':
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

title_pattern = r'<div class="user-title">(.*?)</div>'
play_url_pattern = r'<video id="theVideo" class="video-player" src="(.*?)" preload'


def get(share_url) -> dict:
    result = Result()
    try:
        # get share_url location
        rep1 = requests.get(share_url, headers=headers, timeout=10)
        share_url = rep1.headers.get('location', share_url)

        # get html_text
        rep2 = requests.get(share_url, headers=headers, timeout=10)
        html_text = rep2.text

        title = re.findall(title_pattern, html_text)
        if title:
            result.videoName = title[0]
        play_url = re.findall(play_url_pattern, html_text)
        if play_url:
            play_url = play_url[0].replace('playwm', 'play')

        # get video_url
        rep3 = requests.get(play_url, headers=headers, allow_redirects=False, timeout=30)
        video_url = rep3.headers.get('location')
        if video_url:
            result.videoUrls.append(video_url)
        else:
            result.msg = "视频未能解析成功"


    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()


if __name__ == "__main__":
    data = get(input('share url: '))
    print(data)