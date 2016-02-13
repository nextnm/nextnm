import os
import json

import tornado.ioloop
import tornado.web

# from tornado import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world2")
        routes = load_routes()
        application = tornado.web.Application(routes, **settings)
        # tornado.ioloop.IOLoop.instance().stop()
        # tornado.ioloop.IOLoop.instance().start()

class ProfileHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self, username):
        self.write(self.database[username])


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    # "xsrf_cookies": True,
    "debug" : True
}

def load_routes():
    routes = []
    routes_configs = json.load(open("handlers.json"))
    for routes_cfg in routes_configs:
        if len(routes_cfg) > 2:
            print dict(database=routes_cfg[2])
            routes.append((routes_cfg[0], eval(routes_cfg[1]), dict(database=routes_cfg[2])))
        else:
            routes.append((routes_cfg[0], eval(routes_cfg[1])))
    return routes


routes = load_routes()
application = tornado.web.Application(routes, **settings)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
