"""Limiters in asynciolimiter"""

from __future__ import annotations

from asynciolimiter import (
    LeakyBucketLimiter as _LeakyBucketLimiter,
    Limiter as _Limiter,
    StrictLimiter as _StrictLimiter,
)


class LeakyBucketLimiter(_LeakyBucketLimiter):
    def __init__(self, rate: float, /, *, capacity: int = 10) -> None:
        super().__init__(rate, capacity=capacity)


class Limiter(_Limiter):
    def __init__(self, rate: float, /, *, max_burst: int = 5) -> None:
        super().__init__(rate, max_burst=max_burst)


class StrictLimiter(_StrictLimiter):
    def __init__(self, rate: float, /) -> None:
        super().__init__(rate)
