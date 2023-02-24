from typing import Union

import asyncpg
from aiogram import Bot
from asyncpg.pool import Pool

from tg_bot.config import Config


class Database:
    def __init__(self, config: Config):
        self.pool: Union[Pool, None] = None
        self.config: Config = config

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=self.config.db.user,
            password=self.config.db.password,
            database=self.config.db.database,
            host=self.config.db.host,
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as conn:
            conn: asyncpg.Connection
            async with conn.transaction():
                if fetch:
                    result = await conn.fetch(command, *args)
                elif fetchval:
                    result = await conn.fetchval(command, *args)
                elif fetchrow:
                    result = await conn.fetchrow(command, *args)
                elif execute:
                    result = await conn.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(255) NOT NULL,
            username VARCHAR(255) NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            telegram_id VARCHAR(255) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def select_all_users(self):
        sql = """
        SELECT * FROM users;
        """
        return await self.execute(sql, fetch=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)])
        return sql, tuple(parameters.values())

    async def select_user(self, **kwargs):
        sql = """
        SELECT * FROM users WHERE 
        """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = """
        SELECT COUNT(*) FROM users
        """
        return await self.execute(sql, fetchval=True)

    async def delete_users(self):
        await self.execute("DELETE FROM users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE users", execute=True)
