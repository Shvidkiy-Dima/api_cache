import asyncio
import argparse

from cache import CacheManager
from api import API


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--interval', type=int, default=1,
                        help='How often you want to make request and cache it')
    args = parser.parse_args()

    cache_coroutine = CacheManager.start(url=args.url, interval=args.interval)
    api_coroutine = API.start(port=args.port)

    await asyncio.gather(api_coroutine, cache_coroutine)


if __name__ == '__main__':
    asyncio.run(main())
