def cache_query(func):
    cache = {}

    def wrapper(*args, **kwargs):
        query = args[0] if args else None
        if query in cache:
            print(f"[CACHE HIT] Returning cached result for: {query}")
            return cache[query]
        else:
            print(f"[CACHE MISS] Executing query: {query}")
            result = func(*args, **kwargs)
            cache[query] = result
            return result

    return wrapper

@cache_query
def execute_query(query):
    print(f"[DB] Actually executing: {query}")
    return f"Result for: {query}"

print(execute_query("SELECT * FROM users"))
print(execute_query("SELECT * FROM orders"))
print(execute_query("SELECT * FROM users"))
