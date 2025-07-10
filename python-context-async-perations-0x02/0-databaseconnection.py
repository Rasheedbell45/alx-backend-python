class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        print("[DB] Connection opened.")
        return self

    def close(self):
        print("[DB] Connection closed.")

    def execute(self, query):
        print(f"[DB] Executing query: {query}")
        return f"Results for query: {query}"

if __name__ == "__main__":
    with DatabaseConnection() as db:
        result = db.execute("SELECT * FROM users")
        print(result)
