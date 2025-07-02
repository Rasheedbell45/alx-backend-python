import MySQLdb

def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from the user_data table in batches of `batch_size`
    """
    db = MySQLdb.connect(
        host="localhost",
        user="your_username",
        passwd="your_password",
        db="your_database"
    )
    cursor = db.cursor()

    cursor.execute("SELECT * FROM user_data")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    db.close()
                
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user[2] > 25:
                yield user or

        if user[2] > 25:
                results.append(user)
    return results
          for user in batch_processing(10):
    print(user)
