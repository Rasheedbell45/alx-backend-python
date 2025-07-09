def connect():
    print("[DB] Connection opened.")
    return "db_connection"

def close(connection):
    print(f"[DB] Connection '{connection}' closed.")

def commit(connection):
    print(f"[DB] Transaction committed on '{connection}'.")

def rollback(connection):
    print(f"[DB] Transaction rolled back on '{connection}'.")

def with_db_connection():
    def decorator(func):
        def wrapper(*args, **kwargs):
            connection = connect()
            try:
                return func(connection, *args, **kwargs)
            finally:
                close(connection)
        return wrapper
    return decorator

def transactional(func):
    def wrapper(connection, *args, **kwargs):
        print("[DB] Beginning transaction...")
        try:
            result = func(connection, *args, **kwargs)
            commit(connection)
            return result
        except Exception as e:
            rollback(connection)
            raise e
    return wrapper

@with_db_connection()
@transactional
def run_query(connection, query):
    print(f"[DB] Running: {query}")
    if "FAIL" in query:
        raise Exception("Simulated DB error")
    return "Success"

run_query("SELECT * FROM users")
run_query("FAIL QUERY")
