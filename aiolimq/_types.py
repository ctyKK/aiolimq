"""Type-hint"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from asynciolimiter import _CommonLimiterMixin


V = TypeVar('V')

L = TypeVar('L', bound=_CommonLimiterMixin)
"""Limiter Type"""


@runtime_checkable
class SupportsGtLt(Protocol):
    def __gt__(self, other, /) -> bool: ...
    def __lt__(self, other, /) -> bool: ...


SupportsGtLtV = TypeVar('SupportsGtLtV', bound=SupportsGtLt)
