# coding:utf-8

import datetime
import json

import tornado.gen
import tornado.httpclient
import tornado.web


class XimalayaHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, albumId):
        if albumId and albumId.isdigit():
            client = tornado.httpclient.AsyncHTTPClient()
            url = 'http://mobile.ximalaya.com/mobile/v1/album?albumId={}'.format(albumId)
            response = yield client.fetch(url)

            if response.error:
                raise tornado.web.HTTPError(response.code)
            else:
                ret = json.loads(response.body)['ret']
                data = json.loads(response.body)['data']
                if ret == 0:
                    tracks = data['tracks']['list']
                elif ret == 3:
                    url2 = 'http://mobile.ximalaya.com/mobile/v1/album/track?albumId={}'.format(albumId)
                    response2 = yield client.fetch(url2)
                    data2 = json.loads(response2.body)['data']
                    tracks = data2['list']
                else:
                    self.redirect("/")
                    return
                album = data['album']
                retitle = album['title']
                category = album['categoryName']
                description = album['intro']
                pic = album['coverOrigin']
                items = []
                for card in tracks:
                    item = {}
                    if card.get('playUrl64'):
                        content = card['title']
                        title = card['title']
                        link = "http://m.ximalaya.com/{}/sound/{}".format(card['uid'], card['trackId'])
                        created = card['createdAt'] / 1000
                        created = datetime.datetime.fromtimestamp(created).strftime(
                            "%a, %d %b %Y %H:%M:%S")

                        item['content'] = content
                        item['title'] = title
                        item['link'] = link
                        item['created'] = created
                        item['guid'] = item['link']
                        item['author'] = card['nickname']
                        item['mp3_url'] = card['playUrl64']
                        item['length'] = card['duration']
                        item['pic'] = card['coverMiddle']
                        if card.get('price'):
                            item['title'] = u"{}(试听)".format(title)
                        items.append(item)
                if len(items) > 0:
                    pubdate = items[0]['created']
                    link = "http://m.ximalaya.com/{}/album/{}".format(album['uid'], album['albumId'])
                    self.set_header("Content-Type", "application/xml")
                    self.set_header("Cache-Control", "public, max-age=14400")
                    self.render("podcast_rss.xml", title=retitle, description=description, items=items, pubdate=pubdate,
                                link=link, pic=pic, url=self.request.full_url(), category=category)
                    return
                self.redirect("/")

        else:
            self.redirect("/")


class QingtingHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, albumId):
        if albumId and albumId.isdigit():
            client = tornado.httpclient.AsyncHTTPClient()
            url = "http://api2.qingting.fm/v6/media/channelondemands/{}/programs/order/0/curpage/1/pagesize/100".format(
                albumId)
            url2 = "http://api2.qingting.fm/v6/media/channelondemands/{}".format(albumId)
            response = yield client.fetch(url)
            response2 = yield client.fetch(url2)

            if response.error:
                raise tornado.web.HTTPError(response.code)
            else:
                tracks = json.loads(response.body)['data']
                data2 = json.loads(response2.body)['data']
                retitle = data2['title']
                category = ""
                description = data2['description']
                pic = data2['thumbs']['small_thumb']
                items = []
                for card in tracks:
                    item = {}
                    if len(card.get('mediainfo', {}).get('bitrates_url', [])) > 0:
                        content = card['title']
                        title = card['title']
                        link = "http://www.qingting.fm/channels/{}/programs/{}".format(albumId, card['id'])
                        created = card['update_time']
                        created = datetime.datetime.strptime(created, '%Y-%m-%d %H:%M:%S').strftime(
                            "%a, %d %b %Y %H:%M:%S")

                        item['content'] = content
                        item['title'] = title
                        item['link'] = link
                        item['created'] = created
                        item['guid'] = item['link']
                        item['author'] = data2['title']
                        item['mp3_url'] = "http://od.qingting.fm/{}".format(
                            card.get('mediainfo').get('bitrates_url')[0]['file_path'])
                        item['length'] = card['duration']
                        item['pic'] = pic
                        items.append(item)
                if len(items) > 0:
                    pubdate = datetime.datetime.strptime(data2['update_time'], '%Y-%m-%d %H:%M:%S').strftime(
                        "%a, %d %b %Y %H:%M:%S")
                    link = "http://www.qingting.fm/channels/{}".format(albumId)
                    self.set_header("Content-Type", "application/xml")
                    self.set_header("Cache-Control", "public, max-age=14400")
                    self.render("podcast_rss.xml", title=retitle, description=description, items=items, pubdate=pubdate,
                                link=link, pic=pic, url=self.request.full_url(), category=category)
                    return
                self.redirect("/")

        else:
            self.redirect("/")


class KaolaFMHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, albumId):
        if albumId and albumId.isdigit():
            client = tornado.httpclient.AsyncHTTPClient()
            url = "http://v3.kaolafm.com/api/audioList/{}?pageSize=20&pageNum=1&audioId=".format(
                albumId)
            url2 = "http://v3.kaolafm.com/api/album/{}?pageNum=1&pageSize=1".format(albumId)
            response = yield client.fetch(url)
            response2 = yield client.fetch(url2)

            if response.error:
                raise tornado.web.HTTPError(response.code)
            else:
                tracks = json.loads(response.body)['result']['dataList']
                data2 = json.loads(response2.body)['result']
                retitle = data2['name']
                category = ""
                description = data2['des']
                pic = data2['img']
                items = []
                for card in tracks:
                    item = {}
                    content = card['title']
                    title = card['title']
                    link = "http://m.kaolafm.com/share/jm.html?audioId={}".format(card['audioId'])
                    created = card['updateTime'] / 1000
                    created = datetime.datetime.fromtimestamp(created).strftime(
                        "%a, %d %b %Y %H:%M:%S")

                    item['content'] = content
                    item['title'] = title
                    item['link'] = link
                    item['created'] = created
                    item['guid'] = item['link']
                    item['author'] = card['uploaderName']
                    item['mp3_url'] = card['mp3PlayUrl64']
                    item['length'] = card['duration']
                    item['pic'] = card['pic']
                    items.append(item)
                if len(items) > 0:
                    pubdate = items[0]['created']
                    link = "http://m.kaolafm.com/share/zj.html?albumId={}".format(albumId)
                    self.set_header("Content-Type", "application/xml")
                    self.set_header("Cache-Control", "public, max-age=14400")
                    self.render("podcast_rss.xml", title=retitle, description=description, items=items, pubdate=pubdate,
                                link=link, pic=pic, url=self.request.full_url(), category=category)
                    return
                self.redirect("/")

        else:
            self.redirect("/")
