import asyncio
import time
from slower import Slower


async def test_sequential():
    async with Slower(5, seconds=1) as sem:
        for i in range(100):
            await sem.acquire(1)
            await asyncio.sleep(3)
            print(i, time.monotonic())
            await sem.release(1)
 
async def test_concurrent():
    async def do(i, sem):
        await sem.acquire(1)
        await asyncio.sleep(3)
        print(i, time.monotonic())
        await sem.release(1)

    async with Slower(5, seconds=1) as sem:
        tasks = [do(i, sem) for i in range(20)]
        await asyncio.gather(*tasks)

