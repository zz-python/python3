import sqlite3

db = "logCaUrl.db"

def create_table():
    # 连接到 SQLite 数据库（如果文件不存在，会自动创建）
    conn = sqlite3.connect(db)

    # 创建一个 cursor 对象，用于执行 SQL 操作
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    # 提交事务
    conn.commit()
    conn.close()

def insert_table():
    # 连接到 SQLite 数据库（如果文件不存在，会自动创建）
    conn = sqlite3.connect(db)

    # 创建一个 cursor 对象，用于执行 SQL 操作
    cursor = conn.cursor()
    # 插入一条数据
    cursor.execute('''
        INSERT INTO users (name, age) VALUES (?, ?)
    ''', ("Alice", 30))

    # 提交事务
    conn.commit()

    # 插入多条数据
    users_data = [("Bob", 25), ("Charlie", 35), ("David", 40)]
    cursor.executemany('''
        INSERT INTO users (name, age) VALUES (?, ?)
    ''', users_data)

    # 提交事务
    conn.commit()
    conn.close()

def update_table():
    # 连接到 SQLite 数据库（如果文件不存在，会自动创建）
    conn = sqlite3.connect(db)

    # 创建一个 cursor 对象，用于执行 SQL 操作
    cursor = conn.cursor()

    # 更新数据
    cursor.execute('''
        UPDATE users SET age = ? WHERE name = ?
    ''', (31, 'Alice'))

    # 提交事务
    conn.commit()

    conn.close()

def delete_table():
    # 连接到 SQLite 数据库（如果文件不存在，会自动创建）
    conn = sqlite3.connect(db)

    # 创建一个 cursor 对象，用于执行 SQL 操作
    cursor = conn.cursor()

    # 删除数据
    cursor.execute('DELETE FROM users WHERE name = ?', ("Bob",))

    # 提交事务
    conn.commit()

    conn.close()

def query_table():
    # 连接到 SQLite 数据库（如果文件不存在，会自动创建）
    conn = sqlite3.connect(db)

    # 创建一个 cursor 对象，用于执行 SQL 操作
    cursor = conn.cursor()

    # 查询符合条件的用户
    cursor.execute('SELECT * FROM users WHERE age > ?', (30,))

    # 获取结果
    rows = cursor.fetchall()

    # 打印结果
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    create_table()
    insert_table()
    update_table()
    delete_table()
    query_table()