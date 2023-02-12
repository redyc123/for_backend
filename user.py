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

    history = ""

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
                        eth INT,
                        banned INT,
                        ban_time INT,
                        history STR,
                        count INT);
                        """)
        self.conn.commit()

    async def add_user_db(self, user_id, btc = btc, eth = eth, banned = banned, ban_time = ban_time, history = history, count = user_count):
        user = (user_id, btc, eth, banned, ban_time, history, count)
        await self.create_table()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?);", user
        )
        self.conn.commit()

    async def update_user_db(self, user_id, btc = btc, eth = eth, banned = banned, ban_time = ban_time, history = history, count = user_count):
        user = (user_id, btc, eth, banned, ban_time, history, count)
        cur = self.conn.cursor()
        cur.execute(
            "REPLACE INTO users VALUES(?, ?, ?, ?, ?, ?, ?);", user
        )
        self.conn.commit()

    async def change_money(self, command, user_id):
        current_state = await self.read_table(user_id)
        user = list(current_state)
        text = ""
        if command == "/change_bitcoin":
            if str(user[1]) == "0":
                user[1] = "1"
                text = "bitcoin включен"
            else:
                (user[1]) = "0"
                text = "bitcoin отключен"
        if command == "/change_ethereum":
            if str(user[2]) == "0":
                user[2] = "1" 
                text = "ethereum включен"
            else:
                user[2] = "0"
                text = "ethereum отключен"
        print(user)
        await self.update_user_db(*user)

        return text

    async def change_history(self, history, user_id):
        current_state = await self.read_table(user_id)
        user = list(current_state)
        user[5] = history
        print(user[5])
        await self.update_user_db(*user)

    async def change_banned(self, banned, time, count, user_id):
        current_state = await self.read_table(user_id)
        user = list(current_state)
        user[3] = "1" if banned else "0"
        user[4] = time
        user[6] = count
        await self.update_user_db(*user)

    async def ban(self, user_id, count=user_count):
        if count >= 5:
            self.banned = True
            self.current_time = time.time()
            self.user_count = 0

        self.ban_time = time.time() - self.current_time
        if self.ban_time >= 600:
            self.banned = False
        await self.change_banned(self.banned, self.ban_time, self.user_count, user_id)
        return self.banned