import os

from models.response import Response
from services.bilibili import (SubtitleDownload, bilibili_search, charts,
                               hot_video)


class BiliSearch():
    def __init__(self, input_data: dict):
        self.input_data = input_data

    def run(self):
        try:
            results = bilibili_search(self.input_data)
            return Response(status="success", content=results)

        except Exception as e:
            return Response(status="error", content="", error=str(e))


class BiliHotVideo():

    def run(self):
        try:
            results = hot_video()
            return Response(status="success", content=results)

        except Exception as e:
            return Response(status="error", content="", error=str(e))


class BiliCharts():
    def run(self):
        try:
            results = charts()
            return Response(status="success", content=results)

        except Exception as e:
            return Response(status="error", content="", error=str(e))


class BiliSubtitles():
    def __init__(self, bvid):
        self.bvid = bvid
        self.cookie = os.getenv("BILIBILI_COOKIE")

    def run(self):
        try:
            subtitle = SubtitleDownload(
                self.bvid, 0, self.cookie).download_subtitle()
            return Response(status="success", content=subtitle)
        except Exception as e:
            return Response(status="error", content="", error=str(e))
