def log_queries():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Log the SQL query (assuming first argument is the query string)
            if args:
                print(f"[LOG] Executing SQL Query: {args[0]}")
            else:
                print(f"[LOG] Executing SQL Query: <no query provided>")
            # Call the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def execute_query(query, params=None):
    # Simulated execution
    print(f"Running query: {query}")
    if params:
        print(f"With params: {params}")
    return "Query result"

result = execute_query("SELECT * FROM users WHERE age > %s", [25])

[LOG] Executing SQL Query: SELECT * FROM users WHERE age > %s
Running query: SELECT * FROM users WHERE age > %s
With params: [25]
