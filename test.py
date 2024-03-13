import asyncio
import time
from __init__ import SoftSemaphore


async def sequential_test():
    async with SoftSemaphore(5, seconds=1) as sem:
        for i in range(100):
            await sem.acquire(1)
            print(i, time.monotonic())
            
async def concurrent_test():
    async def do(i, sem):
        await sem.acquire(1)
        print(i, time.monotonic())

    async with SoftSemaphore(5, seconds=1) as sem:
        tasks = [do(i, sem) for i in range(20)]
        await asyncio.gather(*tasks)
            
if __name__ == '__main__':
    asyncio.run(concurrent_test())
