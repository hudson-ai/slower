import asyncio

__all__ = [
    "Slower",
]

class Slower:
    
    def __init__(self, n, seconds=60):
        self.queue = asyncio.Queue(maxsize=n)
        self.lock = asyncio.Lock()
        self.seconds = seconds
        self.tasks = set()

    async def acquire(self, n=1):
        if n > self.queue.maxsize:
            raise ValueError(f"Can't aquire more than {self.queue.maxsize}")
        # Use lock to prevent deadlock
        async with self.lock:
            for i in range(n):
                await self.queue.put(i)

        # Schedule items to be released
        release_task = asyncio.create_task(
            self._release(n)
        )
        # Strong reference to task to prevent garbage collection
        self.tasks.add(release_task)
        # Discard references when done
        release_task.add_done_callback(self.tasks.discard)

    async def _release(self, n):
        await asyncio.sleep(self.seconds)
        for i in range(n):
            self.queue.get_nowait()

    async def close(self):
        # Cancel and clear release_tasks
        for task in self.tasks:
            task.cancel()
        self.tasks = set()
        # Clean up remaining items in the queue
        for i in range(self.queue.qsize()):
            self.queue.get_nowait()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
