import logging
import json
from mysql.connector import MySQLConnection, Error

class Positions:

    def __init__(self, connection: MySQLConnection, positions):
        self.conn = connection
        self.positions = positions

    def rate_transformation(self, position):
        return json.dumps([
            {
                "value": int(position[13][1:]), 
                "currency": f"{position[13][:1]}",
                "startDate": f"{position[3]}",
                "endDate": f"{position[4]}",
                "index": 0
            }
        ]) 

    def get_project_ids(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT id FROM projects")
                result = cursor.fetchall()
                self.conn.commit()
                return [project_id[0] for project_id in result]
        except Error as e:
            logging.error(f"ERROR: {e}")

    def position_validation(self, position, projects_ids):
        id_length = 36
        if (
            len(position) > 0 and
            len(position[1]) == id_length and
            position[9] in projects_ids
        ): 
            return True
    
    def get_query(self, projects_ids):
        s = str()
        for position in self.positions:
            if self.position_validation(position, projects_ids):     
                s += f"('{position[1]}', '{position[2]}', '{position[3]}', '{position[4]}', '{position[9]}', '{self.rate_transformation(position)}')," 
        return "INSERT INTO positions (id, name, start_date, end_date, project_id, rates) VALUES " + s[:-1] + ";"
    
    def insert_projects(self, projects_ids):
        projects_ids = self.get_project_ids()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.get_query(projects_ids))
                self.conn.commit()
            logging.info("Positions. Done!")
        except Error as e:
            logging.error(f"ERROR: {e}")