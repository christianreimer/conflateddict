# Classes to help conflate streaming data

[![Build Status](https://travis-ci.org/christianreimer/conflate.svg?branch=master)](https://travis-ci.org/christianreimer/conflate)  [![Coverage Status](https://coveralls.io/repos/github/christianreimer/conflate/badge.svg?branch=master)](https://coveralls.io/github/christianreimer/conflate?branch=master)  [![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)](https://img.shields.io/badge/python-3.6-blue.svg)

This module contains classes to assist with conflating streaming data. This can
be used to manage the load on conuming tasks, and is especially useful if the
consumers only need the current value and can thus safely discard intermediate
updates.

Why not simply use a new empty dict for each interval? Because many applications require 
all the data when first starting up or connecting (aka initial paint, flatpaint, snapshot, broadcast), and then simply subsequent updates. By using a conflator this paradign can be supported.

### Example
```python
>>> import conflateddict
>>> import random
>>>
>>> keys = ['red', 'green', 'blue', 'orange']
>>> con = conflateddict.ConflatedDict()
>>> for _ in range(100):
...    con[random.choice(keys)] = random.randint(0, 100)
...
>>> print(list(con.items())
[('orange', 32), ('green', 71), ('red', 71), ('blue', 80)]
>>>
>>> # After a reset, there will be no dirty values
>>> con.reset()
>>> print(list(con.items())
[]
>>> # After another update, the dirty values will be returned
>>> con[random.choice(keys)] = random.randint(0, 100)
>>> print(list(con.items())
[('orange', 58)]
>>>
>>> # We still have access to all the values
>>> print(list(con.data().items()))
[('blue', 80), ('red', 71), ('green', 71), ('orange', 58)]
>>>
```


```ConflatedDict``` is a basic conflator that will only return the most recent value.

```OHLCConflator``` is a conflator that will return the Open, High, Low, and Close
values obsered during the interval.

```MeanConflator``` is a conflator that will return the mean of the values observed
during the interval.

```BatchConflator``` is a conflator that will return all the values (in a batch)
observed during the interval.
