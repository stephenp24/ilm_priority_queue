# priority_queue

Welcome to `priority_queue`, a simple implementation for priority queue data structure that utilise python `deque` module.

## Introduction

`priority_queue` typically helpful when the set of data needs to be associated with a certain priority.
This is a simple implementation of priority queue that uses doubly-linked list (`deque` store the data using doubly-linked list). 

> **_NOTE:_** `PQueue` are iterable.

For more implementaion details visit [Technical docs](TECHNICAL.md)

### Requirements

- python `poetry`

### From source

- `git clone` this project
  
  > git clone https://github.com/stephenp24/ilm_priority_queue.git

- `cd` to the ilm_priority_queue dir

  > cd ilm_priority_queue

- `poetry install` and let it find all the requirements

  > `poetry install`

- `poetry run pytest` to run the tests

  > `poetry run pytest . -v`
