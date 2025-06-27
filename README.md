# aiolimq
Asyncio rate-limited queues for Python.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> Based on [asynciolimiter](https://github.com/bharel/asynciolimiter)


## Requirements
- Python >= 3.11
- asynciolimiter >= 1.2.0


## Sample Usage
```python
# cpython-3.13

import asyncio
import random
import string
from datetime import datetime
from aiolimq import LimitedQueue, LimitedPriorityQueue, StrictLimiter


def random_text() -> str:
    return ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 10)))


async def consumer(q: asyncio.Queue, cid: str):
    while True:
        try:
            d = await q.get()
        except asyncio.QueueShutDown:
            return
        else:
            print(datetime.now().strftime('%H:%M:%S.%f')[:11], '\t', cid, '\t', d)
            q.task_done()


async def basic_usage():
    q = LimitedQueue(StrictLimiter(1))

    for _ in range(5):
        q.put_nowait(random_text())

    c = asyncio.create_task(consumer(q, 'basic_usage'))
    await q.join()
    q.shutdown()


async def share_limiter():
    limiter = StrictLimiter(1)
    q1 = LimitedQueue(limiter)
    q2 = LimitedQueue(limiter)

    for _ in range(5):
        q1.put_nowait(random_text())
        q2.put_nowait(random_text())

    c1 = asyncio.create_task(consumer(q1, 'share_limiter-c1'))
    c2 = asyncio.create_task(consumer(q2, 'share_limiter-c2'))

    await asyncio.gather(q1.join(), q2.join())
    q1.shutdown(), q2.shutdown()


async def custom_priority():
    # priority#1 | priority#2 | not-priority
    q: asyncio.Queue[tuple[int, str, int | None]] = LimitedPriorityQueue(
        StrictLimiter(1), lambda _: (_[0], _[1])
    )

    def random_int_none() -> int | None:
        if random.randint(0, 9) >= 5:
            return None
        return random.randint(1, 100)

    for _ in range(10):
        q.put_nowait((random.randint(-100, 100), random_text(), random_int_none()))

    c1 = asyncio.create_task(consumer(q, 'custom_priority-c1'))
    c2 = asyncio.create_task(consumer(q, 'custom_priority-c2'))

    await q.join()
    q.shutdown()


async def custom_priority2():
    # Distance from the 'K'
    q: asyncio.Queue[str] = LimitedPriorityQueue(StrictLimiter(1), lambda _: abs(ord(_) - ord('K')))

    for _ in range(10):
        q.put_nowait(random.choice(string.ascii_uppercase))

    c = asyncio.create_task(consumer(q, 'custom_priority2'))

    await q.join()
    q.shutdown()


async def main():
    print('====================\n\n')

    await basic_usage()
    print('\n\n====================\n\n')

    await share_limiter()
    print('\n\n====================\n\n', end='')

    await custom_priority()
    print('\n\n====================\n\n', end='')

    await custom_priority2()
    print('\n\n====================\n\n', end='')


if __name__ == '__main__':
    asyncio.run(main())
```
