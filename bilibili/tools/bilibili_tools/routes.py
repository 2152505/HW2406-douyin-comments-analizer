from flask import Blueprint, jsonify, request

from errors.errors import InvalidAPIUsage
from tools.bilibili_tools.jobs import (BiliCharts, BiliHotVideo, BiliSearch,
                                       BiliSubtitles)

bili_tools = Blueprint('bilibili_tools', __name__)


@bili_tools.route('/search', methods=['GET'])
def api_fetch_bilibili_videos():
    keyword = request.args.get('keyword', '默认关键词')
    time_duration = request.args.get(
        'time_duration', 1)

    input_data = {
        'keyword': keyword,
        'time_duration': int(time_duration)
    }

    job = BiliSearch(input_data)
    response = job.run()

    if response.is_error():
        raise InvalidAPIUsage(
            "Error searching Bilibili", 500, response.to_dict())

    return jsonify(response.content)


@bili_tools.route('/hot', methods=['GET'])
def api_fetch_hot_videos():
    job = BiliHotVideo()
    response = job.run()

    if response.is_error():
        raise InvalidAPIUsage(
            "Error searching Bilibili", 500, response.to_dict())

    return jsonify(title_urls=response.content)


@bili_tools.route('/chart', methods=['GET'])
def api_fetch_chart_videos():
    job = BiliCharts()
    response = job.run()

    if response.is_error():
        raise InvalidAPIUsage(
            "Error searching Bilibili", 500, response.to_dict())

    return jsonify(title_urls=response.content)


@bili_tools.route('/subtitle', methods=['GET'])
def api_get_subtitle():
    bvid = request.args.get('bvid')
    if not bvid:
        raise InvalidAPIUsage(
            "Missing bvid parameter", 400)

    response = BiliSubtitles(bvid).run()

    if response.is_error():
        raise InvalidAPIUsage(
            "Error in getting subtitles", 500, response.to_dict()
        )

    return jsonify(subtitles=response.content)
