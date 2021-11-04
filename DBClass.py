from datetime import datetime
import sqlite3
import datetime


class DBClass:
    def __init__(self, db_path, camera_name) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cur = self.connection.cursor()

        self.camera_name = camera_name
    
    def new_record(self, **kwargs):
        command = f"INSERT INTO {self.camera_name}(datetime, map) VALUES('{datetime.datetime.now()}', '{kwargs['map']}');"
        self.cur.execute(command)
        self.connection.commit()
    
    def get_camera_params(self) -> dict:
        res = self.cur.execute(f"SELECT * FROM params WHERE name = '{self.camera_name}';").fetchone()
        column_names = [desc[0] for desc in self.cur.description]
        return dict(zip(column_names, res))
    
    def close(self):
        self.connection.close()
    
    @staticmethod
    def activate():
        from local_params import db_params
        return DBClass(**db_params)
