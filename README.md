# Classes to help conflate streaming data

[![Build Status](https://travis-ci.org/christianreimer/conflateddict.svg?branch=master)](https://travis-ci.org/christianreimer/conflateddict)  [![Coverage Status](https://coveralls.io/repos/github/christianreimer/conflateddict/badge.svg?branch=master)](https://coveralls.io/github/christianreimer/conflateddict?branch=master)  [![PyPI version](https://badge.fury.io/py/conflateddict.svg)](https://badge.fury.io/py/conflateddict)   ![Python Version 3.6](https://img.shields.io/badge/python-3.6-blue.svg) ![Python Version 3.7](https://img.shields.io/badge/python-3.7-blue.svg)



This module contains classes to assist with conflating streaming data. This can
be used to manage the load on consuming tasks, and is especially useful if the
consumers only need the current value and can thus safely discard intermediate
updates.

Why not simply use a new empty dict for each interval? Because many applications require 
all the data when first starting up or connecting (aka initial paint, flatpaint, snapshot, broadcast), and then simply subsequent updates. By using a conflator this paradigm can be supported.

## Installation
```bash
$ pip install conflateddict
```

```ConflatedDict``` is a basic conflator that will only return the most recent value.

```OHLCConflator``` is a conflator that will return the Open, High, Low, and Close (last) 
values observed during the interval.

```MeanConflator``` is a conflator that will return the mean of the values observed
during the interval.

```BatchConflator``` is a conflator that will return all the values (in a batch)
observed during the interval.
 
```LambdaConflator``` takes a user provided function of the form ```f(v, vl) -> cv``` where v is the current value and vl is the list of past values observed during the interval and returns the conflated value cv.

```ModeConflator``` is a conflator that will return the mode (most common) value observed during an interval.


## ConflatedDict Example

Use a ConflatedDict if you have a system where the consumer only needs the most
recent value and intermediate values can be skipped. For example, if you are
displaying the data on a dashboard, you only want to show the most recent value.

```python
>>> import conflateddict
>>> import random
>>>
>>> keys = ['red', 'green', 'blue', 'orange']
>>> cd = conflateddict.ConflatedDict()
>>> for _ in range(100):
...    cd[random.choice(keys)] = random.randint(0, 100)
...
>>> print(list(cd.items())))
[('orange', 32), ('green', 71), ('red', 71), ('blue', 80)]
>>> print(len(cd))
4
>>>
```

After a reset, there will be no dirty values
```python
>>> cd.reset()
>>> print(list(cd.items())
[]
>>> print(len(cd))
0
>>>
```

After another update, any new dirty values will be returned
```python
>>> cd[random.choice(keys)] = random.randint(0, 100)
>>> print(list(cd.items()))
[('orange', 58)]
>>> print(len(cd))
1
>>>
```

If you need access to all the values for an initial paint/broadcast you can still access them through the data method.

```python
>>> print(len(cd.data()))
4
>>> for key, value in cd.data().items()
...     print(key, value)
...
orange 58
green 71
red 71
blue 80
>>>
```

## BatchConflator Example
Use a BatchConflator if you have a system with streaming data and consumers
that want to consumes chunks or mini-batches of this data. For example, if you
want to deliver a batch of data for processing every second.

```python
>>> import conflateddict
>>> import random
>>> import time
>>>
>>> keys = ['red', 'green', 'blue', 'orange']
>>> bc = conflateddict.BatchConflator()
>>>
>>> last_flush = 0
>>> while True:
...     bc[random.choice(keys)] = random.randint(0, 100)
...     time.sleep(random.random())
...     if time.time() - last_flush > 1:
...         print(list(bc.items()))
...         bc.clear()
...         last_flush = time.time()
[('orange', [21])]
[('blue', [36, 20]), ('red', [56, 70]), ('green', [6])]
[('orange', [88]), ('green', [27])]
[('red', [30]), ('orange', [43, 18]), ('green', [40])]
[('red', [92]), ('orange', [45])]
[('blue', [78, 85]), ('red', [83])]
[('blue', [97]), ('green', [64])]
^C
>>>
```

## OHLCConflator Example
Use a OHLCConflator if you have a system with streaming data and consumers
that want to check if a condition has been breached such as checking for a new
lower or upper bound.

```python
>>> import conflateddict
>>> import random
>>> import time
>>>
>>> keys = ['red', 'green', 'blue', 'orange']
>>> oc = conflateddict.OHLCCloflator()
>>>
>>> # Initial values. This would typically just be zero, but for this example
>>> # they are initialized to avoid all events from firing in the first
>>> # iteration of the loop.
>>> prev_ohlc = {key:tuple((random.randint(0, 100) for _ in range(4)))
...     for key in keys}
...
>>>
>>> for _ in range(5):
...     # Generate some data
...     for _ in range(random.randint(1, 10)):
...         oc[random.choice(keys)] = random.randint(0, 100)
...
...     # Check if we have reached new highs/lows
...     for key in keys:
...         try:
...             ohlc = oc[key]
...         except KeyError:
...             continue
...
...         o, h, l, c = prev_ohlc[key]
...
...         if ohlc.low < l:
...             print(f'{key} hit new low of {ohcl.low}')
...             l = ohlc.low
...         if ohlc.high > h:
...             print(f'{key} hit new high of {ohcl.high}')
...             h = ohlc.high
...         if ohlc.open < ohlc.close:
...             print(f'{key} tending higher')
...         if ohlc.open > ohlc.close:
...             print(f'{key} trending lower')
...
...         prev_ohlc[key] = (ohlc.open, h, l, ohlc.close)
...
...     oc.clear()
...
red trending lower
blue hit new high of 49
orange tending higher
green hit new low of 44
green hit new high of 49
green tending higher
blue hit new low of 44
blue tending higher
orange hit new high of 49
red hit new low of 44
red trending lower
green hit new low of 44
green trending lower
blue hit new high of 49
blue trending lower
orange trending lower
red tending higher
orange hit new low of 44
orange tending higher
>>>
```
