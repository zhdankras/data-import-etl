import logging
from mysql.connector import MySQLConnection, Error

class Accounts:

    def __init__(self, connection: MySQLConnection, accounts):
        self.conn = connection
        self.accounts = accounts

    def accounts_validation(self, account):
        id_length = 36
        if (
            len(account) > 0 and 
            len(account[0]) == id_length
        ): 
            return True
    
    def get_query(self):
        s = str()
        for account in self.accounts:
            if self.accounts_validation(account): 
                s += f"('{account[0]}', '{account[1]}', (SELECT au.id  FROM auth_users au WHERE au.username = 'administrator'), '2021/01/01 00:00:00'),"
        return "INSERT INTO accounts (id, name, created_by, created_at) VALUES " + s[:-1] + ";"
    
    def insert_accounts(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.get_query())
                self.conn.commit()
            logging.info("Accounts. Done!")
        except Error as e:
            logging.error(f"ERROR: {e}")