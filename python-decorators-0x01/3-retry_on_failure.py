import time

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"[Attempt {attempt}] Running {func.__name__}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    last_exception = e
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
            print("All retries failed.")
            raise last_exception
        return wrapper
    return decorator

count = 0

@retry_on_failure(retries=3, delay=1)
def unstable_db_operation():
    global count
    count += 1
    print("Attempting risky DB operation...")
    if count < 3:
        raise Exception("Transient DB error")
    print("Operation succeeded.")
    return "Success"

result = unstable_db_operation()
print("Final result:", result)
