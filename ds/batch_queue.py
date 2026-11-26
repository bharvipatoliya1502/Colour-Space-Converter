"""A simple FIFO queue for batch image conversion jobs."""

from collections import deque


class BatchQueue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if not self._items:
            raise IndexError("Cannot dequeue from an empty queue.")
        return self._items.popleft()

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)
