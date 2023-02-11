import sqlite3

import time

class User():
    def __init__(self) -> None:
        pass
    user_count = 0
    banned = False
    current_time = 0
    conn = sqlite3.connect("base/users.db")

    btc = '1'
    eth = '1'
    ban_time = 0

    async def read_table(self, user_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id={user_id};")
        one_result = cur.fetchone()
        return one_result

    async def create_table(self):
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INT PRIMARY KEY,
                        btc INT,
                        eth INT);
                        """)
        self.conn.commit()

    async def add_user_db(self, user_id, btc = btc, eth = eth):
        user = (user_id, btc, eth)
        await self.create_table()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO users VALUES(?, ?, ?);", user
        )
        self.conn.commit()

    async def update_user_db(self, user_id, btc = btc, eth = eth):
        user = (user_id, btc, eth)
        cur = self.conn.cursor()
        cur.execute(
            "REPLACE INTO users VALUES(?, ?, ?);", user
        )
        self.conn.commit()

    async def change_money(self, command, user_id):
        current_state = await self.read_table(user_id)
        user = list(current_state)
        text = ""
        if command == "/change_bitcoin":
            if str(user[1]) == "0":
                user[1] = "1" 
            else:
                (user[1]) = "0"
            text = "bitcoin изменен"
        if command == "/change_ethereum":
            if str(user[2]) == "0":
                user[2] = "1" 
            else:
                user[2] = "0"
            text = "ethereum изменен"
        print(user)
        await self.update_user_db(user[0], user[1], user[2])

        return text

    async def ban(self, count=user_count):
        if count >= 5:
            self.banned = True
            self.current_time = time.time()
            self.user_count = 0

        self.ban_time = time.time() - self.current_time
        if self.ban_time >= 600:
            self.banned = False
        return self.banned