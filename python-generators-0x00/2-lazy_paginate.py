import MySQLdb

def paginate_users(page_size, offset):
    """
    Fetch one page of users from the database at a given offset.
    """
    db = MySQLdb.connect(
        host="localhost",
        user="your_username",
        passwd="your_password",
        db="your_database"
    )
    cursor = db.cursor()
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results


def lazy_paginate(page_size):
    """
    Generator that yields pages of user data lazily.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

  for page in lazy_paginate(5):
    for user in page:
        print(user)
