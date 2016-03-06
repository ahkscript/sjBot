#!/usr/bin/env python3


import urllib.parse
import json


aliases = ['ytb', 'y', 'yt']


def youtube(con, sjBot, commands, trigger, host, channel, *query):
    """Searches youtube for a video"""
    api_key = sjBot['settings']['google_key']
    download = sjBot['url_download']
    query_string = urllib.parse.quote(' '.join(query))
    query_url = ('https://www.googleapis.com/youtube/v3/search?key={}'
                '&part=id,snippet&q={}'.format(api_key, query_string))
    result_data = download(query_url)
    youtube_data = json.loads(result_data)
    try:
        item = youtube_data['items'][0]
        title = item['snippet']['title']
        vid_id = item['id']['videoId']
        vid_url = 'https://youtu.be/{}'.format(vid_id)
    except Exception:
        return 'Could not find info for that video.'
    return '\x02{}\x02 - {}'.format(title, vid_url)