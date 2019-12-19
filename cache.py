import asyncio
from dataclasses import dataclass, asdict
from typing import Optional, Any
from aiohttp import ClientSession, ClientResponse


@dataclass
class Cache:
    body: bytes
    content_type: str = 'application/json'
    status: int = 200
    reason: Optional[Any] = 'OK'
    charset: Optional[str] = 'utf-8'


class CacheManager:
    _cache = Cache(content_type='application/json',
                   body=b'{"message": "Cache not set yet"}',
                   status=403)

    @classmethod
    async def start(cls, url, interval):
        while True:
            cls._cache = await cls._handle_client_response(url)
            await asyncio.sleep(interval)

    @classmethod
    def get_cache(cls) -> dict:
        return asdict(cls._cache)

    @classmethod
    async def _handle_client_response(cls, url) -> Cache:
        async with ClientSession() as session:
            async with session.get(url) as resp:
                cache = await cls._retrieve_cache_from_response(resp)

        return cache

    @classmethod
    async def _retrieve_cache_from_response(cls, response: ClientResponse) -> Cache:
        body = await response.read()
        cache = Cache(body=body,
                      reason=response.reason,
                      content_type=response.content_type,
                      status=response.status,
                      charset=response.charset)
        return cache
