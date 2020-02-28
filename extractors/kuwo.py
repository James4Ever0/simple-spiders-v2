import re

import requests

from extractors.result import Result
from extractors.errors import errors, NotFoundException, ServerErrorException


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.1516764754.1579334008; _gid=GA1.2.8717020.1579334008; _gat=1; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1579334010; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1579334010; kw_token=MJ3PBY3HDNP',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
}

song_info_url = 'http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={id}'
mp3_url = 'http://www.kuwo.cn/url?format=mp3&rid={id}&response=url&type=convert_url3&br={quality}&from=web'


def get(url: str) -> dict:
    result = Result()
    try:
        id = re.findall(r'([0-9]{1,})', url)
        if id:
            id = id[0]
        else:
            raise NotFoundException

        # 得到最高品质以及歌曲信息
        rep = requests.get(song_info_url.format(id=id), headers=headers, timeout=11)
        if rep.status_code == 200:
            best_quality = rep.json().get('data').get('songinfo').get('coopFormats')[0]
            author = rep.json().get('data').get('songinfo').get('artist')
            song_name = rep.json().get('data').get('songinfo').get('songName')
            result.author = author
            result.audioName = song_name

        if not best_quality: best_quality = '128kmp3'

        # 得到歌曲链接
        rep2 = requests.get(mp3_url.format(id=id, quality=best_quality))
        if rep2.status_code == 200:
            play_url = rep.json().get('url', '')
            result.audioUrls.append(play_url)
        else:
            result.msg = "歌曲链接没能得到"
    except errors as e:
        result.err = 1
        result.msg = e.message

    return result()


if __name__ == "__main__":
    print(get(input('url:  ')))