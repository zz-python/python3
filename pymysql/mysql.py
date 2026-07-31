# -*- coding: utf-8 -*-
"""
PyMySQL 数据库操作封装类

提供 MySQL 数据库连接、查询所有表、获取表描述等常用功能。
"""

import pymysql
from pymysql.cursors import DictCursor
from typing import Any


class MySQL:
    """MySQL 数据库操作封装类"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "",
        charset: str = "utf8mb4",
        autocommit: bool = True,
    ):
        """
        初始化 MySQL 连接配置

        :param host: 数据库主机地址
        :param port: 数据库端口
        :param user: 用户名
        :param password: 密码
        :param database: 默认数据库名
        :param charset: 字符集
        :param autocommit: 是否自动提交
        """
        self._config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": charset,
            "autocommit": autocommit,
            "cursorclass": DictCursor,
        }
        self._conn: pymysql.Connection | None = None

    # ------------------------------------------------------------------
    # 连接管理
    # ------------------------------------------------------------------

    def connect(self) -> "MySQL":
        """建立数据库连接"""
        if self._conn is None or not self._conn.open:
            self._conn = pymysql.connect(**self._config)
        return self

    def close(self):
        """关闭数据库连接"""
        if self._conn and self._conn.open:
            self._conn.close()
            self._conn = None

    def is_connected(self) -> bool:
        """检查连接是否可用"""
        return self._conn is not None and self._conn.open

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    @property
    def _cursor(self):
        """获取游标，确保连接可用"""
        if not self.is_connected():
            self.connect()
        return self._conn.cursor()

    def _execute(self, sql: str, params: tuple | None = None) -> Any:
        """执行 SQL 并返回游标"""
        cursor = self._cursor
        cursor.execute(sql, params)
        return cursor

    # ------------------------------------------------------------------
    # 查询所有表
    # ------------------------------------------------------------------

    def get_tables(self, database: str | None = None) -> list[str]:
        """
        获取指定数据库中的所有表名

        :param database: 数据库名，不传则使用连接时配置的默认库
        :return: 表名列表
        """
        db = database or self._config["database"]
        if not db:
            raise ValueError("未指定数据库名")

        sql = "SHOW TABLES"
        if db:
            sql = f"SHOW TABLES FROM `{db}`"

        cursor = self._execute(sql)
        # SHOW TABLES 返回的列名形如 Tables_in_<db>
        rows = cursor.fetchall()
        return [list(row.values())[0] for row in rows]

    def get_all_tables(self, database: str | None = None) -> list[str]:
        """get_tables 的别名"""
        return self.get_tables(database)

    # ------------------------------------------------------------------
    # 表描述（DESCRIBE / SHOW COLUMNS）
    # ------------------------------------------------------------------

    def describe_table(self, table: str, database: str | None = None) -> list[dict]:
        """
        获取表的字段描述信息（等价于 DESCRIBE table）

        :param table: 表名
        :param database: 数据库名，不传则使用默认库
        :return: 字段描述列表，每项包含 Field, Type, Null, Key, Default, Extra
        """
        db = database or self._config["database"]
        full_name = f"`{db}`.`{table}`" if db else f"`{table}`"

        cursor = self._execute(f"DESCRIBE {full_name}")
        return cursor.fetchall()

    def get_columns(self, table: str, database: str | None = None) -> list[dict]:
        """describe_table 的别名"""
        return self.describe_table(table, database)

    # ------------------------------------------------------------------
    # 获取所有表及其描述
    # ------------------------------------------------------------------

    def get_all_tables_with_descriptions(
        self, database: str | None = None
    ) -> dict[str, list[dict]]:
        """
        获取所有表名及其字段描述

        :param database: 数据库名
        :return: {表名: [字段描述列表]}
        """
        tables = self.get_tables(database)
        db = database or self._config["database"]
        result = {}
        for table in tables:
            result[table] = self.describe_table(table, db)
        return result

    # ------------------------------------------------------------------
    # 常用查询
    # ------------------------------------------------------------------

    def query(self, sql: str, params: tuple | None = None) -> list[dict]:
        """执行查询 SQL，返回所有结果"""
        cursor = self._execute(sql, params)
        return cursor.fetchall()

    def query_one(self, sql: str, params: tuple | None = None) -> dict | None:
        """执行查询 SQL，返回第一条结果"""
        cursor = self._execute(sql, params)
        return cursor.fetchone()

    def execute(self, sql: str, params: tuple | None = None) -> int:
        """执行写操作（INSERT/UPDATE/DELETE），返回影响行数"""
        cursor = self._execute(sql, params)
        self._conn.commit()
        return cursor.rowcount

    def get_databases(self) -> list[str]:
        """获取所有数据库名"""
        cursor = self._execute("SHOW DATABASES")
        return [row["Database"] for row in cursor.fetchall()]


# ------------------------------------------------------------------
# 简易使用示例
# ------------------------------------------------------------------

if __name__ == "__main__":
    # 方式一：with 语句（推荐）
    with MySQL(host="10.51.134.53", user="root", password="password", database="database") as db:
        # 获取所有表
        tables = db.get_tables()
        print("表数量:", len(tables))
        print("所有表:", tables)

        # # 获取某张表的描述
        # if tables:
        #     desc = db.describe_table(tables[0])
        #     print("表描述:", desc)

        # 获取所有表及其描述
        # all_info = db.get_all_tables_with_descriptions()
        # print("所有表及描述:", all_info)

    # 方式二：手动管理连接
    # db = MySQL(host="localhost", user="root", password="123456", database="test")
    # db.connect()
    # tables = db.get_tables()
    # db.close()
