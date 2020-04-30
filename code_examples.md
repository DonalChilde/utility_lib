# Code Examples

filtering a list of dicts

```python
# also matches if "published" key is not present.
# returns a list
if published_only:
    return [item for item in data if bool(item.get("published", True))]

# returns a generator
# consider this when working with large data sets.
if published_only:
    return (item for item in data if bool(item.get("published", True)))

```

Temp directories in pytest

```python
import pytest
# Place this in the conftest.py file,
# and customize the test directory based on project name.

@pytest.fixture(scope="session")
def test_log_path(tmp_path_factory):
    log_path = tmp_path_factory.mktemp("eve_esi_")
    return log_path

```

Logging in pytest

```python
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pytest

# Place this in the test file, customize library loggers as needed.

@pytest.fixture(scope="module")
def logger(test_log_path):
    log_file_name = f"{__name__}.log"
    _logger = logging.getLogger(__name__)
    log_path = test_log_path / Path("test-logs")
    log_level = logging.DEBUG
    if not log_path.exists():
        log_path.mkdir(parents=True)
    file_handler = RotatingFileHandler(
        log_path / Path(log_file_name), maxBytes=102400, backupCount=10
    )
    format_string = "%(asctime)s %(levelname)s:%(funcName)s: %(message)s [in %(pathname)s:%(lineno)d]"
    file_handler.setFormatter(logging.Formatter(format_string))
    file_handler.setLevel(log_level)
    _logger.addHandler(file_handler)
    _logger.setLevel(log_level)
    ############################################################
    # NOTE add file handler to other library modules as needed #
    ############################################################
    # async_logger = logging.getLogger("eve_esi.utility_lib.async_queue")
    async_logger = logging.getLogger("eve_esi")
    async_logger.setLevel(log_level)
    async_logger.addHandler(file_handler)
    return _logger

```

Combine a list of lists

```python
from itertools import chain
from typing import Any, List

data: List[List[Any]] = [[1,2,3,4],[5,6,7,8]]
combined_iterator = chain(*data)
combined_list = list(combined_iterator)

```

Chunk a list

```python
from more_itertools import chunked
type_ids = range(500)
chunked_types_ids = chunked(type_ids, 200)

```

sort a list of objects

# https://docs.python.org/3/howto/sorting.html

```python
# https://docs.python.org/3/howto/sorting.html
from operator import itemgetter, attrgetter

data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
sorted_data = sorted(data, key=itemgetter(0))
# [('blue', 1), ('blue', 2), ('red', 1), ('red', 2)]

# to reverse add reverse=True, ie
# sorted_data = sorted(data, key=itemgetter(0), reverse=True)

# can use multiple sort criteria
def multisort_sequence_get_item(xs, specs):
    # sorts list in place
    for key, reverse in reversed(specs):
        xs.sort(key=attrgetter(key), reverse=reverse)
    return xs

def multisort_sequence_get_attr(xs, specs):
    # sorts list in place
    for key, reverse in reversed(specs):
        xs.sort(key=attrgetter(key), reverse=reverse)
    return xs

```

"slice" a dict

```python
for item in islice(result.items(), 2):
    print(item)
```
