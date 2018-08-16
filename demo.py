import aiohttp, asyncio


async def fn(num):
    async with aiohttp.get(
            url='https://www.liaoxuefeng.com/discuss/001409195742008d822b26cf3de46aea14f2b7378a1ba91000?page={}'.format(
                    num)) as resp:
        text = await resp.text()
