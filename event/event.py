"""
This module implements a simple event system for this application.
"""
from enum import Enum, auto

subscribers: dict[str, list] = {}


class EventType(Enum):
    paddle_up = auto()
    paddle_down = auto()


def subscribe(event_type: EventType, fn) -> None:
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(fn)


def post_event(event_type: EventType, data) -> None:
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)
