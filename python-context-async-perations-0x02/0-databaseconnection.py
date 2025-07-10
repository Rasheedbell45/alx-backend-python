class DatabaseConnection:
    def __enter__(self):
        self.connection = self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(self.connection)

    def connect(self):
        print("[DB] Connection opened.")
        return self

    def close(self, connection):
        print("[DB] Connection closed.")

    def execute(self, query):
        print(f"[DB] Executing query: {query}")
        return f"Results for query: {query}"

with DatabaseConnection() as db:
    result = db.execute("SELECT * FROM users")
    print(result)
