# -*- coding: UTF-8 -*-
#/*
# *      Copyright (C) 2015 Josef Weiss
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import re,os,urllib,urllib2,cookielib
import json,xbmcplugin
import requests
from provider import ContentProvider

class SlowTVContentProvider(ContentProvider):

    def __init__(self,username=None,password=None,filter=None):
        ContentProvider.__init__(self,
                                 'slowtv.playtvak.cz',
                                 'http://servis.idnes.cz/ExportApi/playtvak.aspx',
                                 username,
                                 password,
                                 filter)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        urllib2.install_opener(opener)

    def capabilities(self):
        return ['resolve','categories']

    def categories(self):
        result = []

        url = "http://servis.idnes.cz/ExportApi/playtvak.aspx"
        querystring = {"t":"articleassemblylist","id":"n4_slowtv_slowtv","page":"1","onpage":"30"}
        headers = {'cache-control': "no-cache"}
        response = requests.request("GET", url, headers=headers, params=querystring)

        json_data = json.loads(response.content)

        articles = json_data["result"]["articleList"]["articles"]

        for article in articles:
            item = self.video_item()
            item['title'] = article["title"] + " 720p"
            item['img'] = article["photo"]["types"][0]["url"]
            item['url'] = article["videoGallery"]["video"][0]["videoFiles"][0]["link"]
            result.append(item)

            item1 = self.video_item(item)
            item1['title'] = article["title"] + " 360p"
            item1['url'] = article["videoGallery"]["video"][0]["videoFiles"][1]["link"]
            result.append(item1)
        return result

    def resolve(self,item,captcha_cb=None,select_cb=None):
        return self.video_item(url=item['url'])