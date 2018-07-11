# Classes to help conflate streaming data

[![Build Status](https://travis-ci.org/christianreimer/conflateddict.svg?branch=master)](https://travis-ci.org/christianreimer/conflateddict)  [![Coverage Status](https://coveralls.io/repos/github/christianreimer/conflateddict/badge.svg?branch=master)](https://coveralls.io/github/christianreimer/conflateddict?branch=master)  ![Python Version 3.6](https://img.shields.io/badge/python-3.6-blue.svg) ![Python Version 3.7](https://img.shields.io/badge/python-3.7-blue.svg)



This module contains classes to assist with conflating streaming data. This can
be used to manage the load on consuming tasks, and is especially useful if the
consumers only need the current value and can thus safely discard intermediate
updates.

Why not simply use a new empty dict for each interval? Because many applications require 
all the data when first starting up or connecting (aka initial paint, flatpaint, snapshot, broadcast), and then simply subsequent updates. By using a conflator this paradigm can be supported.

### Installation
```bash
$ pip install --index-url https://test.pypi.org/simple/ conflateddict
```


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
>>> print(len(con))
4
>>> # After a reset, there will be no dirty values
>>> con.reset()
>>> print(list(con.items())
[]
>>> print(len(con))
0
>>> # After another update, any new dirty values will be returned
>>> con[random.choice(keys)] = random.randint(0, 100)
>>> print(list(con.items())
[('orange', 58)]
>>>
>>> # We still have access to all the values through data()
>>> print(list(con.data().items()))
[('blue', 80), ('red', 71), ('green', 71), ('orange', 58)]
>>> print(len(con.data()))
4
>>>
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
