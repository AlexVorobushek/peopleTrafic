from datetime import datetime
import sqlite3
import datetime


class DBClass:
    def __init__(self, db_path, table_name) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cur = self.connection.cursor()

        self.table_name = table_name
    
    def new_imprinting(self, **kwargs):
        command = f"INSERT INTO {self.table_name}(datetime, map) VALUES('{datetime.datetime.now()}', '{kwargs['map']}');"
        self.cur.execute(command)
        self.connection.commit()
    
    def get_all(self):
        return self.cur.execute(f"SELECT * FROM {self.table_name};")
    
    def close(self):
        self.connection.close()
    
    @staticmethod
    def activate():
        from params import db_params
        return DBClass(**db_params)