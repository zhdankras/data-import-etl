import logging
from mysql.connector import MySQLConnection, Error

class Assignments:

    def __init__(self, connection: MySQLConnection, assignments):
        self.conn = connection
        self.assignments = assignments

    def get_users_email(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT email FROM users")
                result = cursor.fetchall()
                self.conn.commit()
                return [email[0] for email in result]
        except Error as e:
            logging.error(f"ERROR: {e}")
    
    def get_positions_ids(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT id FROM positions")
                result = cursor.fetchall()
                self.conn.commit()
                return [position_id[0] for position_id in result]
        except Error as e:
            logging.error(f"ERROR: {e}")

    def assignment_validation(self, assignment, positions_ids, users_emails):
        id_length = 36 
        if (
            len(assignment) > 0 and
            len(assignment[0]) == id_length and
            len(assignment[8]) == id_length and
            len(assignment[2]) > 0 and
            assignment[8] in positions_ids and
            assignment[2] in users_emails
        ): 
            return True

    def get_query(self, positions_ids, users_emails):
        s = str()
        for assignment in self.assignments:
            if self.assignment_validation(assignment, positions_ids, users_emails) == True:
                s += f"('{assignment[0]}', (select id from users where email = '{assignment[2]}'), '{assignment[8]}', '{assignment[10][:-4]}', '{assignment[11][:-4]}', '{assignment[12]}', '{assignment[13]}'),"
        return "INSERT INTO assignments (id, user_id, position_id, billed_involvement, involvement, start_date, end_date) VALUES " + s[:-1] + ";"
    
    def insert_assignments(self):
        positions_ids = self.get_positions_ids()
        users_emails = self.get_users_email()
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.get_query(positions_ids, users_emails))
                self.conn.commit()
            logging.info("Assignments. Done!")
        except Error as e:
            logging.error(f"ERROR: {e}")