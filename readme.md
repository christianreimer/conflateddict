### Classes to help conflate streaming data

Use a simple ```Conflator``` if you have streaming key=value pairs and you
only want to transmit (or update) based on the most recent value in the stream.

If you care about the most extreme values for a key, then use a ```OHLCConflator``` to conflate the stream. For example, streaming stock prices can be conflated so that each update will still produce the open, high, low, and close values.
