#!/usr/bin/env python3


import re
import json


muted_channels = []


def r_PRIVMSG(con, sjBot, user, channel, *message):
    print('Youtube')
    if channel in muted_channels:
        return None
    print('youtube')
    video_match = re.search('(yout.*v=|yout.*/)(.*?)(\&|\s+|$|#|\?)',
                            ' '.join(message))
    print( video_match.group(2) )
    if video_match is None:
        return None
    video_id = video_match.group(2)
    google_key = sjBot['settings']['google_key']
    download = sjBot['url_download']
    result = download('https://www.googleapis.com/youtube/v3/videos?id={}'
                      '&key={}&part=snippet,contentDetails,statistics,'
                      'status'.format(video_id, google_key))
    video_data = json.loads(result)
    item = video_data['items'][0]
    title = item['snippet']['title']
    time = (item['contentDetails']['duration'].replace('PT', '')
            .replace("S", "").replace("H", ":").replace('M', ':').split(":"))
    for i, v in enumerate(time):
        time[i] = '{0:02d}'.format(int(v))
    time = ':'.join(time)
    if ':' not in time:
        time = time + ' seconds'
    #viewcount = int(item['statistics']['viewCount'])
    #likecount = int(item['statistics']['likeCount'])
    #dislikecount = int(item['statistics']['dislikeCount'])
    nickname = user.split('!')[0][1:]
    con.privmsg(channel, "[{}'s link] \x02{}\x02 - {}".format(nickname, title,
                time))
    return None