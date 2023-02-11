import aiohttp

import asyncio

async def get_price(money) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.coingecko.com/api/v3/simple/price?ids={money}&vs_currencies=usd&precision=1') as resp:
            m = await resp.json()
            return m

BTC = asyncio.run(get_price("bitcoin"))["bitcoin"]["usd"]
ETH = asyncio.run(get_price("ethereum"))["ethereum"]["usd"]

monyes = {
    "bitcoin": BTC,
    "ethereum": ETH
}