"""Type-hint"""

from __future__ import annotations

from typing import Callable, Protocol, TypeVar, runtime_checkable

from asynciolimiter import _CommonLimiterMixin


V = TypeVar('V')

L = TypeVar('L', bound=_CommonLimiterMixin)
"""Limiter"""


@runtime_checkable
class SupportsGtLt(Protocol):
    """Support __gt__ and __lt__"""

    def __gt__(self, other, /) -> bool: ...
    def __lt__(self, other, /) -> bool: ...


S = TypeVar('S', bound=SupportsGtLt)
"""Support __gt__ and __lt__"""

P = Callable[[V], S]
"""Priority calculator"""
