import pytest

import asyncio
import time
from more_itertools import sliding_window

from slower import Slower

def no_faster_than(times, n, seconds):
    for window in sliding_window(sorted(times), n):
        if (window[-1] - window[0]) < seconds:
            return False
    return True

def no_slower_than(times, n, seconds):
    for window in sliding_window(sorted(times), n):
        if (window[-1] - window[0]) > seconds:
            return False
    return True

async def do(response_time, s: Slower):
    # Simulate a response from a server.
    await s.acquire()
    recieve_time = time.monotonic()
    await asyncio.sleep(response_time)
    return recieve_time

@pytest.mark.parametrize("n", (1, 10, 100, 1000))
@pytest.mark.parametrize("seconds", (.1, .5, 1))
@pytest.mark.parametrize("response_time", (0, .1, .5))
async def test_slower(n, seconds, response_time):
    async with Slower(n, seconds) as s:
        jobs = [do(response_time, s) for _ in range(2*n)]
        times = await asyncio.gather(*jobs)
    assert no_faster_than(times, n+1, seconds)
    assert no_slower_than(times, n, seconds + .1)