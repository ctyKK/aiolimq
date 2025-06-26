"""Queues"""

from __future__ import annotations

import heapq
from asyncio import Queue
from typing import Generic

from asynciolimiter import _CommonLimiterMixin

from ._types import L, P, S, V


class LimitedQueue(Queue[V], Generic[L, V]):
    """Limited asyncio.Queue"""

    def __init__(self, limiter: L, maxsize: int = 0) -> None:
        super().__init__(maxsize=maxsize)

        if not isinstance(limiter, _CommonLimiterMixin):
            raise TypeError(type(limiter).__name__)

        self._limiter = limiter

    async def put(self, item: V) -> None:
        return await super().put(item)

    async def get(self) -> V:
        await self._limiter.wait()
        return await super().get()


class LimitedPriorityQueue(LimitedQueue[L, V], Generic[L, S, V]):
    """Limited priority asyncio.Queue"""

    def __init__(self, limiter: L, priority: P[V, S] = lambda _: _, maxsize: int = 0) -> None:  # type: ignore
        super().__init__(limiter, maxsize)

        self._priority: P[V, S] = priority
        """Priority calculator"""
        self._auto_id: int = 0
        """Auto increment ID"""

    def _init(self, maxsize: int) -> None:
        self._queue: list[tuple[S, int, V]] = list()

    def _put(self, item: V, heappush=heapq.heappush) -> None:
        entity = (self._priority(item), self._auto_id, item)
        heappush(self._queue, entity)
        self._auto_id += 1

    def _get(self, heappop=heapq.heappop) -> V:
        _, _, item = heappop(self._queue)
        return item
