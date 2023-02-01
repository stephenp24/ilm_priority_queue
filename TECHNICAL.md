# Implementation

Following as the estimate complexity for each operation that `PQueue` supports:

| function | complexity (from worst case) |
| -------- | --------- |
| append | O(N) |
| remove | O(1) |
| pop | O(1) |

## Why deque?

The decision to utilise deque for priority queue implementation comes from the fact that:
- Optimised for queue access.
  - Accessing both ends is O(1)
  - Insertion is O(1)
- ``deque`` is already part of stdlib 
- proven to be performant and thread-safe, this avoids having to reimplement the wheel

## Future consideration

Additional consideration:
- Custom ``WorkItem`` class to handle all validation, however this would mean our queue won't work with python built-ins dict
- Using descriptor for custom ``WorkItem`` class to handle the type validation for both commands and priority key 
- Using ``WorkItem`` might also be easier to add support for dynamic priority changes
