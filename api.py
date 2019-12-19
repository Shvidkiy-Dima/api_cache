from aiohttp import web
from cache import CacheManager


class API:

    @classmethod
    def start(cls, port):
        app = web.Application()
        app.router.add_routes([web.get('/', cls._get_cache)])
        return web._run_app(app, port=port)  # pylint: disable=W0212

    @classmethod
    async def _get_cache(cls, _):
        cache = CacheManager.get_cache()
        response = cls.make_response_from_cache(cache)
        return response

    @classmethod
    def make_response_from_cache(cls, cache: dict) -> web.Response:
        response = web.Response(**cache)
        return response
