import asyncio
import aiosqlite

DB_FILE = "users.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n[ALL USERS]")
    for row in all_users:
        print(row)

    print("\n[USERS OLDER THAN 40]")
    for row in older_users:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
