import os

from gevent import monkey

monkey.patch_all()

PORT = int(os.environ['LEANCLOUD_APP_PORT'])

# _basedir = os.path.abspath(os.path.dirname(__file__))
# if _basedir not in sys.path:
#     sys.path.insert(0, _basedir)
#
# reload(sys)
# sys.setdefaultencoding('utf-8')

import tornado.ioloop
import tornado.wsgi

from jinja2_tornado import JinjaLoader
from urls import urls
from leancloud import Engine

applications = tornado.wsgi.WSGIApplication(
    handlers=urls,
    static_path=os.path.join('static'),
    template_loader=JinjaLoader(os.path.join('templates'),
                                autoescape=True, extensions=['jinja2.ext.autoescape']),
    debug=False,
)

engine = Engine(applications)
application = engine

if __name__ == "__main__":
    applications.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
