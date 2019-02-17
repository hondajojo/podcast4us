import os
import sys

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in sys.path:
    sys.path.insert(0, _basedir)

# reload(sys)
# sys.setdefaultencoding('utf-8')

import tornado.ioloop
import tornado.web

from jinja2_tornado import JinjaLoader
from urls import urls

PORT = int(os.environ.get('PORT', 5000))

application = tornado.web.Application(
    handlers=urls,
    static_path=os.path.join(_basedir, 'static'),
    template_loader=JinjaLoader(os.path.join(_basedir, 'templates'),
                                autoescape=True, extensions=['jinja2.ext.autoescape']),
    debug=True,
)

if __name__ == "__main__":
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
