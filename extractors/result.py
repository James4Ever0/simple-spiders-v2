class Result(object):

    def __init__(self):
        self.err = 0
        self.msg = "success"
        self.author = ""
        self.videoName = ""
        self.audioName = ""
        self.imgUrls = []
        self.audioUrls = []
        self.videoUrls = []
        self.text = ""

    def __call__(self) -> dict:
        data = {
            "err": self.err,
            "msg": self.msg,
            "author": self.author,
            "videoName": self.videoName,
            "audioName": self.audioName,
            "imgUrls": self.imgUrls,
            "audioUrls": self.audioUrls,
            "videoUrls": self.videoUrls,
            "text": self.text,
        }
        return data