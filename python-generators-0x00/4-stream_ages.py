import MySQLdb

def stream_user_ages():
    """
    Generator to lazily fetch and yield user ages from the user_data table.
    """
    db = MySQLdb.connect(
        host="localhost",
        user="your_username",
        passwd="your_password",
        db="your_database"
    )
    cursor = db.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row[0]

    cursor.close()
    db.close()

def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")

# Call the main function
compute_average_age()
