import udsoncan
import time

def retry_until_success(operation, max_attempts=7, delay=1.0):
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except udsoncan.exceptions.TimeoutException as e:
            print(f"Attempt {attempt}/{max_attempts}: ECU not responding yet ({e})")
            time.sleep(delay)
    raise RuntimeError("ECU did not come back after reset")

def retry_with_backoff(delay=2, retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_retry = 0
            current_delay = delay
            while current_retry < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    current_retry += 1
                    if current_retry >= retries:
                        raise e
                    print(f"Failed to execute function '{func.__name__}'. Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= 2
        return wrapper
    return decorator