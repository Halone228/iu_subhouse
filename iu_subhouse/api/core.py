from falcon.asgi import App
from .sources import *


class HealthResource:
    async def on_get(self, req, resp): # noqa
        resp.status = 200
        resp.text = 'ok'


def create_app():
    app = App()
    app.add_route("/source", SourcesResource())
    app.add_route("/healthy", HealthResource())
    return app
