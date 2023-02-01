import mock
import pytest
from priority_queue import COMMAND_KEY, PRIORITY_KEY, PQueue


def test_queue():
    """Test basic queue behaviour"""
    # ARRANGE: Create a queue
    p = PQueue()

    # ASSERT: empty queue
    assert not p
    assert len(p) == 0

    # ACT: append a new item
    item = {COMMAND_KEY: "foo", PRIORITY_KEY: 10}
    p.append(item)

    # ASSERT: queue items contain item
    assert item in p

    # ASSERT: non-empty queue
    assert bool(p)
    assert len(p) == 1


def test_remove():
    """Test ``remove()`` removes the item from the queue"""
    # ARRANGE: Create a queue with couple items
    p = PQueue()
    item_0 = {COMMAND_KEY: "foo", PRIORITY_KEY: 10}
    item_1 = {COMMAND_KEY: "bar", PRIORITY_KEY: 20}
    item_2 = {COMMAND_KEY: "baz", PRIORITY_KEY: 30}
    p.append(item_0)
    p.append(item_1)
    p.append(item_2)

    # ASSERT: All item is in the queue
    assert list(p) == [item_0, item_1, item_2]

    # ACT: remove items
    p.remove(item_1)
    assert list(p) == [item_0, item_2]
    p.remove(item_0)
    assert list(p) == [item_2]
    p.remove(item_2)
    assert list(p) == []


def test_append():
    """Test ``append()`` stores the item as expected"""
    # ARRANGE: Create a queue
    q = PQueue()
    test_item = {COMMAND_KEY: "foo", PRIORITY_KEY: 10}

    # ACT: append the item
    q.append(test_item)

    # ASSERT: item should be inserted as expected
    expected_items = [dict(command="foo", priority=10)]
    assert list(q) == expected_items

    # ARRANGE: update the item
    test_item[COMMAND_KEY] = "bar"
    test_item[PRIORITY_KEY] = 100
    test_item["foo"] = mock.ANY

    # ASSERT: updated item shouldn't affect the queue work items
    assert list(q) == expected_items

    # ACT: append items with additional unrelated-keys
    q.append(test_item)

    # ASSERT: item should be inserted as expected
    expected_items.append(dict(command="bar", priority=100))
    assert list(q) == expected_items


def test_append_raises():
    """Test ``append()`` raises expected exception on validation"""
    # ARRANGE: Create a queue
    q = PQueue()

    # ASSERT: appending non dict instance should raise TypeError
    with pytest.raises(TypeError) as err:
        # ACT:
        q.append(mock.ANY)
        assert "Invalid item type" in str(err)

    # ASSERT: missing dict key item should raise KeyError
    with pytest.raises(KeyError) as err:
        # ACT:
        q.append({COMMAND_KEY: mock.ANY})
        assert "Missing key item: ``priority``" == str(err)

    # ASSERT: non-string command should raise ValueError
    with pytest.raises(ValueError) as err:
        # ACT:
        q.append({COMMAND_KEY: mock.ANY, PRIORITY_KEY: 0})
        assert "Invalid ``command`` type, expected str" in str(err)

    # ASSERT: non-int priority should raise ValueError
    with pytest.raises(ValueError) as err:
        # ACT:
        q.append({COMMAND_KEY: "foo", PRIORITY_KEY: mock.ANY})
        assert "Invalid ``priority`` type, expected int" in str(err)

    # ASSERT: negative int priority should raise ValueError
    with pytest.raises(ValueError) as err:
        # ACT:
        q.append({COMMAND_KEY: "foo", PRIORITY_KEY: -10})
        assert "Invalid ``priority`` value, expected positive int" in str(err)


def test_sorted():
    """Test ``append()`` sorted the item based on priority as expected"""
    # ARRANGE: Sample of unordered priority
    priority_list = [5, 4, 6, 7, 7, 3, 0, 10, 7, 1, 2, 8]

    # ACT: append
    q = PQueue()
    for idx, priority in enumerate(priority_list):
        item = {
            COMMAND_KEY: f"at index: {str(idx)}",
            PRIORITY_KEY: priority,
        }
        q.append(item)

    # ASSERT: work items are ordered based on priority
    expected_work_items = [
        # Lowest priority ordered at the begining of work items
        {PRIORITY_KEY: 0, COMMAND_KEY: "at index: 6"},
        {PRIORITY_KEY: 1, COMMAND_KEY: "at index: 9"},
        {PRIORITY_KEY: 2, COMMAND_KEY: "at index: 10"},
        {PRIORITY_KEY: 3, COMMAND_KEY: "at index: 5"},
        {PRIORITY_KEY: 4, COMMAND_KEY: "at index: 1"},
        {PRIORITY_KEY: 5, COMMAND_KEY: "at index: 0"},
        {PRIORITY_KEY: 6, COMMAND_KEY: "at index: 2"},
        {PRIORITY_KEY: 7, COMMAND_KEY: "at index: 3"},
        # Same priority is ordered based on insertion time
        {PRIORITY_KEY: 7, COMMAND_KEY: "at index: 4"},
        {PRIORITY_KEY: 7, COMMAND_KEY: "at index: 8"},
        {PRIORITY_KEY: 8, COMMAND_KEY: "at index: 11"},
        # Highest priority ordered at the end of the work items
        {PRIORITY_KEY: 10, COMMAND_KEY: "at index: 7"},
    ]
    assert list(q) == expected_work_items

    # ASSERT: ``pop()`` returns the highest priority
    assert q.pop() == dict(priority=10, command="at index: 7")
