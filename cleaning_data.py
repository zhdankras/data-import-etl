import logging
from mysql.connector import MySQLConnection, Error

query = """
    SET FOREIGN_KEY_CHECKS=0;
    DELETE FROM accounts;
    DELETE FROM projects;
    DELETE FROM positions;
    DELETE FROM assignments;
    SET FOREIGN_KEY_CHECKS=1;
"""

class Cleaning: 
    def __init__(self, connection: MySQLConnection):
        self.conn = connection
    
    def cleaning_tables(self):
        try:
            with self.conn.cursor() as cursor:
                results = cursor.execute(query, multi=True)
                [
                    cur for cur in results
                ]
                self.conn.commit()
            logging.info("Clean completed!")
        except Error as e:
            logging.error(f"ERROR: {e}")