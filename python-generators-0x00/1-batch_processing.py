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
    """
    Generator that processes batches and yields users over the age of 25
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user[2] > 25:  # assuming the 3rd column is age
                yield user

          for user in batch_processing(10):
    print(user)
