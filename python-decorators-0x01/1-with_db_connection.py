def connect():
    # Simulate a database connection
    print("[DB] Connection opened.")
    return "db_connection_object"

def close(connection):
    # Simulate closing the database connection
    print(f"[DB] Connection '{connection}' closed.")

def with_db_connection():
    def decorator(func):
        def wrapper(*args, **kwargs):
            connection = connect()
            try:
                # Pass the connection as the first argument
                return func(connection, *args, **kwargs)
            finally:
                close(connection)
        return wrapper
    return decorator

@with_db_connection()
def execute_query(conn, query):
    print(f"Using connection: {conn}")
    print(f"Executing: {query}")

execute_query("SELECT * FROM users;")
