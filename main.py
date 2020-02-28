import re
import time
from enum import Enum
from typing import List

from fastapi import FastAPI
from starlette.responses import HTMLResponse
from pydantic import BaseModel

from extractors import \
    bilibili, changya, douyin, kuwo, lizhiFM, music163, pipigaoxiao, quanminkge, weibo, weishi, zhihu_video, zuiyou_voice

app = FastAPI()


class Extractor(str, Enum):
    bilibili = "bilibili"
    changya = "changya"
    douyin = "douyin"
    kuwo = "kuwo"
    lizhiFM = "lizhiFM"
    pipigaoxiao = "pipigaoxiao"
    quanminkge = "quanminkge"
    weibo = "weibo"
    weishi = "weishi"
    zhihu_video = "zhihu_video"
    zuiyou_voice = "zuiyou_voice"
    music163 = "music163"


class ResponseMode(BaseModel):
    err: int
    msg: str
    author: str
    videoName: str
    audioName: str
    imgUrls: List[str]
    audioUrls: List[str]
    videoUrls: List[str]
    text: str
    time: str


@app.get("/{extractor}/", response_model=ResponseMode)
def extract(extractor: Extractor, url: str):
    url_re = r'(https?://[-A-Za-z0-9+&@#/%?=~|!:,.;]+[-A-Za-z0-9+&@#/%=~|])'
    url = re.findall(url_re, url)
    if url:
        url = url[0]
        result = eval(extractor.value).get(url)
    else:
        result = dict(
            err=1,
            msg="invalid link!",
            author="",
            videoName="",
            audioName="",
            imgUrls=[],
            audioUrls=[],
            videoUrls=[],
            text="",
        )

    result["time"] = str(int(time.time()))
    print(result)
    return result
