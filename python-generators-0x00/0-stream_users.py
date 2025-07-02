import MySQLdb

def stream_users():
    """Yields rows from the user_data table one by one using a generator."""
    db = MySQLdb.connect(
        host="localhost",      
        user="your_username",
        passwd="your_password",
        db="your_database"
    )
    cursor = db.cursor()

    cursor.execute("SELECT * FROM user_data")
    
    for row in cursor:
        yield row

    cursor.close()
    db.close()
