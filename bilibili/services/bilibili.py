import re
from collections import Counter

import requests
from bilibili_api import hot, rank, search, sync, video_zone


class SubtitleDownload:

    def __init__(self, bvid: str, page, cookie: str):
        self.bvid = bvid
        self.page = 0
        self.pagelist_api = "https://api.bilibili.com/x/player/pagelist"
        self.subtitle_api = "https://api.bilibili.com/x/player/v2"
        self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'cookie': cookie,
        }

    def _get_player_list(self):
        response = requests.get(self.pagelist_api, params={
                                'bvid': self.bvid}, headers=self.headers)
        cid_list = [x['cid'] for x in response.json()['data']]
        return cid_list

    def _get_subtitle_list(self, cid: str):
        params = (
            ('bvid', self.bvid),
            ('cid', cid),
        )
        response = requests.get(
            self.subtitle_api, params=params, headers=self.headers)
        # print(response.json())
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            n = 1

            for x in subtitles:
                print(str(n) + '.' + x['lan_doc'])
                n = n+1
            m = 1
            return ['https:' + subtitles[m-1]['subtitle_url']]
        else:
            print("获取字幕列表失败，当前没有可下载的字幕，或检查cookie是否正确")
            return None
        return []

    def _get_subtitle(self, cid: str):
        subtitles = self._get_subtitle_list(cid)
        if subtitles:
            return self._request_subtitle(subtitles[0])

    def _request_subtitle(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()['body']
            return body

    def download_subtitle(self):
        # self.__init__()
        self.page = 0
        subtitle_list = self._get_subtitle(self._get_player_list()[self.page])
        if subtitle_list:
            text_list = [x['content'] for x in subtitle_list]
            text = ','.join(text_list)

            return text
        else:
            text = "该视频没有可供下载的字幕"
            return text


class SubtitleDownloadError(Exception):
    pass


def bilibili_search(input_data):
    keyword = input_data.get('keyword', '默认关键词')
    duration = input_data.get('time_duration', 1)  # 如果未提供time_duration，默认为1

    raw_result = sync(search.search_by_type(
        keyword,
        search_type=search.SearchObjectType.VIDEO,
        order_type=search.OrderVideo.TOTALRANK,
        time_range=duration,
        video_zone_type=video_zone.VideoZoneTypes.TECH,
        page=1
    ))

    tags = []
    titles = []
    urls = []
    if 'result' in raw_result:
        for video in raw_result['result'][:10]:
            title = video.get('title', '无标题')
            url = video.get('arcurl', '无url')
            urls.append(url)

            # 清理HTML标签
            title = re.sub(r'<em class="keyword">(.+?)</em>', r'\1', title)
            title = re.sub(r'<[^>]*>', '', title)
            titles.append(title)

            video_tags = video.get('tag', '').split(',')
            tags.extend(tag.strip() for tag in video_tags if tag.strip())

    tag_counts = Counter(tags)
    top_ten_tags = tag_counts.most_common(20)
    top_tags_only = [tag for tag, count in top_ten_tags]
    titles_urls = list(zip(titles, urls))

    return {
        'titles_urls': titles_urls,
        'top_tags': top_tags_only
    }


def hot_video():
    raw_result = sync(hot.get_hot_videos())
    titles = []
    urls = []
    if 'list' in raw_result:
        for video in raw_result['list'][:10]:
            title = video.get('title', '无标题')
            url = video.get('short_link_v2', '无url')
            urls.append(url)

            title = re.sub(r'<em class="keyword">(.+?)</em>',
                           r'\1', title)  # 仅替换特定的带属性的标签，保留内部文本
            title = re.sub(r'<[^>]*>', '', title)  # 移除所有其它HTML标签
            titles.append(title)

    # 统计标签出现次数

    titles_urls = list(zip(titles, urls))
    return titles_urls


def charts():
    raw_result = sync(rank.get_rank())
    titles = []
    urls = []
    if 'list' in raw_result:
        for video in raw_result['list'][:10]:
            title = video.get('title', '无标题')
            url = video.get('short_link_v2', '无url')
            urls.append(url)

            title = re.sub(r'<em class="keyword">(.+?)</em>',
                           r'\1', title)  # 仅替换特定的带属性的标签，保留内部文本
            title = re.sub(r'<[^>]*>', '', title)  # 移除所有其它HTML标签
            titles.append(title)

    # 统计标签出现次数

    titles_urls = list(zip(titles, urls))
    return titles_urls
#