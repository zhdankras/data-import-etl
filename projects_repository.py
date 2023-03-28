import logging
from mysql.connector import MySQLConnection, Error

class Projects:

    def __init__(self, connection: MySQLConnection, projects):
        self.conn = connection
        self.projects = projects

    def get_account_ids(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT id FROM accounts")
                result = cursor.fetchall()
                self.conn.commit()
                return [account_id[0] for account_id in result]
        except Error as e:
            logging.error(f"ERROR: {e}")
    
    def projects_validation(self, project, accounts_ids):
        id_length = 36
        if (
            len(project) > 0 and
            len(project[0]) == id_length and
            project[2] in accounts_ids
        ): 
            return True
    
    def get_query(self, accounts_ids):
        s = str()
        for project in self.projects:
            if self.projects_validation(project, accounts_ids):     
                s += f"('{project[0]}', '{project[1]}', '{project[2]}', '2021/01/01 00:00:00', '2040/12/31 00:00:00')," 
        return "INSERT INTO projects (id, name, account_id, start_date, end_date) VALUES " + s[:-1] + ";"
    
    def insert_projects(self, account_ids):
        accounts_ids = self.get_account_ids()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.get_query(accounts_ids))
                self.conn.commit()
            logging.info("Projects. Done!")
        except Error as e:
            logging.error(f"ERROR: {e}")