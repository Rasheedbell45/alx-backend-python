class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.result = None

    def __enter__(self):
        self.connection = self.connect()
        self.result = self.execute(self.query, self.params)
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        print("[DB] Connection opened.")
        return self

    def close(self):
        print("[DB] Connection closed.")

    def execute(self, query, params):
        print(f"[DB] Executing query: {query} with params {params}")
        return f"Mocked results for: {query} with params {params}"

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as result:
        print(result)

import sqlite3

class ExecuteQuery:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect("mydb.sqlite3")
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
