import time
from datetime import datetime
from functools import wraps

def log_execution(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        current_time=datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] Running: {func.__name__}()")
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(f"Timer: {func.__name__}() took{end - start:.4f}")
        return result
    return wrapper