# coding:utf-8

from handlers import index, ximalaya

urls = [
    (r"/", index.MainHandler),
    (r"/xmly/(\d+).xml", ximalaya.XimalayaHandler),
    (r"/qt/(\d+).xml", ximalaya.QingtingHandler),
    (r"/kl/(\d+).xml", ximalaya.KaolaFMHandler),
]
