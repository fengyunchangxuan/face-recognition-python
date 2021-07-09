import sqlite3


class User:
    """用户类，用于操作sqlite3"""

    # 初始化
    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()
        print('Opened db successfully')

    def create(self):
        """创建用户表"""

        self.cursor.execute('''CREATE TABLE USER
                (ID  INTEGER NOT NULL,
                NAME TEXT NOT NULL);''')

        print('Table created successfully')

    def insert(self, id, name):
        """插入一条用户数据"""

        self.cursor.execute("INSERT INTO USER (ID,NAME) \
        VALUES (%d,'%s')" % (id, name))
        print('Insert one record')

    def delete(self, id):
        """更新一条数据"""

        self.cursor.execute("DELETE from USER where id = %d" % id)
        print('Delete one record')

    def update(self, id, name=''):
        """更新一条数据"""

        # 四个属性都为空，直接返回
        if not name:
            print('No record')
            return None

        execute = "UPDATE USER set NAME = '%s' where ID=%d" % (name, id)
        self.cursor.execute(execute)
        print('Update one record')

    def select(self):
        """查询数据"""

        rows = self.cursor.execute('SELECT  id,name FROM USER')
        return rows

    def select_name(self, id):
        """查询数据"""

        rows = self.cursor.execute('SELECT name FROM USER where id = %d' % id)
        return rows

    def close(self):
        """关闭db"""

        self.db.commit()
        self.db.close()
