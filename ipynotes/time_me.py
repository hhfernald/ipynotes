#!/usr/bin/env python3

import time
from functools import wraps

def time_me(label):
    def time_me__decorator(func):
        """Prints a label and the number of msec it took to run a function."""
        
        @wraps(func)
        def time_me__function_wrapper(*args, **kw):
            startTime = int(round(time.time() * 1000))
            result = func(*args, **kw)
            endTime = int(round(time.time() * 1000))

            print(label, endTime - startTime,'ms')
            return result
        return time_me__function_wrapper
    return time_me__decorator


