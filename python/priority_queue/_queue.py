""" 
"""
__all__ = [
    "PQueue",
]

import logging
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from functools import wraps
from itertools import groupby
from typing import TYPE_CHECKING, Deque, Dict, Generator, Union, cast

from six import string_types

from ._constant import COMMAND_KEY, PRIORITY_KEY
from ._logger import get_logger

_LOGGER = get_logger(__name__, level=logging.DEBUG)


def validate_item(func):
    """A decorator to validate the input item.
    A "valid" item refers to:

        - ``item`` instance type must be a built-ins dict
        - ``item`` must have at least both "command" and "priority" key
        - ``item`` "command" must be a str type
        - ``item`` "priority" must be a positive real numbers

    .. note:: Any other item keys is ignored.

    """

    @wraps(func)
    def wrapper(queue, item: Dict[str, Union[str, int]]):
        # ``item`` instance type must be a built-ins dict
        if not isinstance(item, dict):
            raise TypeError(f"Invalid item type: ``{type(item)}``")

        # ``item`` must have at least both "command" and "priority" key
        missing_key = {COMMAND_KEY, PRIORITY_KEY}.difference(set(item.keys()))
        if missing_key:
            raise KeyError(f"Missing key item: ``{missing_key}``")

        # ``item`` "command" must be a str type
        if not isinstance(item[COMMAND_KEY], string_types):
            raise ValueError(
                f"Invalid ``{COMMAND_KEY}`` type, expected str, received {type(item[COMMAND_KEY])}"
            )

        # ``item`` "priority" must be a positive int type
        if not isinstance(item[PRIORITY_KEY], int):
            raise ValueError(
                f"Invalid ``{PRIORITY_KEY}`` type, expected int, received {type(item[PRIORITY_KEY])}"
            )
        # Note: Cast to int for python type checking
        if cast(int, item[PRIORITY_KEY]) < 0:
            raise ValueError(
                f"Invalid ``{PRIORITY_KEY}`` value, expected positive int, recieved {item[PRIORITY_KEY]}"
            )

        # Return a deepcopy of work item to avoid mutability problem when dealing with dict
        item = {
            PRIORITY_KEY: item[PRIORITY_KEY],
            COMMAND_KEY: deepcopy(item[COMMAND_KEY]),
        }
        func(queue, item)

    return wrapper


@dataclass(eq=False)
class PQueue:
    """Priority Queue implementation using doubly linked list.

    .. warning:: This does not supports dynamic changes of the work item priorities.

    """

    #: Private data container, user shouldn't have to deal with this
    __work_items: Deque = field(default_factory=deque, repr=False)

    # ----- dunder -----

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(work_items={self.__work_items})"

    def __bool__(self) -> bool:
        return len(self.__work_items) > 0

    def __len__(self) -> int:
        return len(self.__work_items)

    def __iter__(self) -> Generator:
        for item in self.__work_items:
            yield item

    def __contains__(self, item) -> bool:
        return item in self.__work_items

    # ----- utility functions -----

    @validate_item
    def append(self, item: Dict[str, Union[str, int]]) -> None:
        """Append a new work item to the queue.

        .. note:: The inserted item are ordered based on priority from the lowest the highest

        .. note:: Any changes on the ``item`` instance is ignored once the item is inserted to
            the queue.

        Args:
            item (Dict[str, Union[str, int]]): The work item to be inserted into the queue.
                A work item is expected to have the two following keys:

                    - "command"
                    - "priority"
        """
        # New item
        if not self.__work_items:
            self.__work_items.appendleft(item)
        # Lowest priority item
        elif item[PRIORITY_KEY] < self.__work_items[0][PRIORITY_KEY]:
            self.__work_items.appendleft(item)
        # Highest priority item
        elif item[PRIORITY_KEY] >= self.__work_items[-1][PRIORITY_KEY]:
            self.__work_items.append(item)
        # Mid item, sort based on priority
        else:
            # find the index where it should be added, worst case is O(N-1)
            # Note: At this point we know for sure its not higher than the last
            #       last item, so it won't raise ``StopIteration`` exception.
            mid_index_item = next(
                filter(
                    lambda cur_item: cur_item[PRIORITY_KEY] > item[PRIORITY_KEY],
                    self.__work_items,
                )
            )
            mid_index = self.__work_items.index(mid_index_item)
            self.__work_items.insert(mid_index, item)

    @validate_item
    def remove(self, item: Dict[str, Union[str, int]]) -> None:
        """Remove the given ``item`` from the queue."""
        if item in self.__work_items:
            self.__work_items.remove(item)

    def pop(self) -> None:
        """Retrieve the highest priority item and remove it from the queue"""
        return self.__work_items.pop()
