from datetime import datetime

def connect():
    # Simulate connecting to a database
    print("[DB] Connected to database.")

def log_queries():
    def decorator(func):
        def wrapper(*args, **kwargs):
            connect()
            if args:
                print(f"[{datetime.now()}] Executing SQL Query: {args[0]}")
            else:
                print(f"[{datetime.now()}] Executing SQL Query: <no query provided>")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def run_query(query):
    print(f"Running: {query}")

run_query("SELECT * FROM users WHERE active = 1")
