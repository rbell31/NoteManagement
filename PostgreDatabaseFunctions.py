import os.path
import json
import psycopg2 as pg
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



class SqlActions:
    def __init__(self, database, table):
        self.DB_NAME = database
        self.TB_NAME = table

    def create_database(self):
        return sql.SQL('CREATE DATABASE {}').format(sql.Identifier(self.DB_NAME))

    def drop_database(self):
        return sql.SQL('DROP DATABASE IF EXISTS {}').format(sql.Identifier(self.DB_NAME))

    def new_table(self):
        return sql.SQL('CREATE TABLE IF NOT EXISTS {}').format(sql.Identifier(self.TB_NAME))

    def new_image_insert(self):
        return sql.SQL('INSERT INTO {} ').format(sql.Identifier(self.TB_NAME))




class PostgreInstance:

    def __init__(self, **kwargs):
        # HARD CODE LOGIN FILE
        dirname = os.path.dirname(__file__)
        login_file = os.path.join(dirname, 'login.json')
        with open(login_file, 'r') as reader:
            self.LOGIN = json.load(reader)

        if kwargs:
            host = kwargs.get('host')
            db = kwargs.get('dbname')
            if host and db:
                print('host - db')
                self.connection = pg.connect(user=self.LOGIN.get('user'),
                                             password=self.LOGIN.get('password'),
                                             host=host,
                                             database=db)
            elif host:
                print('host')
                self.connection = pg.connect(user=self.LOGIN.get('user'),
                                             password=self.LOGIN.get('password'),
                                             host=host)
            elif db:
                print('db')
                self.connection = pg.connect(user=self.LOGIN.get('user'),
                                             password=self.LOGIN.get('password'),
                                             database=db)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()
        else:
            self.connection = pg.connect(user=self.LOGIN.get('user'),
                                         password=self.LOGIN.get('password'))
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()



DB_NAME = 'notes'

post = PostgreInstance()
commands = SqlActions(DB_NAME)


post.cursor.execute(commands.create_database())
post.cursor.close()
post.connection.close()