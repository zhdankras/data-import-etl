import logging
from mysql.connector import connect, Error
from cleaning_data import Cleaning
from export import export_data
from accounts_repository import Accounts
from projects_repository import Projects
from positions_repository import Positions
from assignments_repository import Assignments

def main():

    try:

        mysql_connection = connect(
            host=os.environ.get('HOST_NAME'),
            port=os.environ.get('PORT'),
            user=os.environ.get('ROOT'),
            password=os.environ.get('PASS'),
            database=os.environ.get('DB') 
        )
        
        logging.info(f"Database connection was successful!")

    except Error as e:
        logging.error(f"Database connection failed: {e}")
    
    Cleaning(mysql_connection).cleaning_tables()
    Accounts(mysql_connection, export_data('1xujOhv45Q4Hdt6kOTHEfuI_ucHXY4IVBmN5tuhwYvII', 'DATA - Accounts')).insert_accounts()
    Projects(mysql_connection, export_data('1xujOhv45Q4Hdt6kOTHEfuI_ucHXY4IVBmN5tuhwYvII', 'DATA - Projects')).insert_projects()
    Positions(mysql_connection, export_data('1xujOhv45Q4Hdt6kOTHEfuI_ucHXY4IVBmN5tuhwYvII', 'DATA - Positions')).insert_positions()
    Assignments(mysql_connection, export_data('1xujOhv45Q4Hdt6kOTHEfuI_ucHXY4IVBmN5tuhwYvII', 'DATA - Assignments')).insert_assignments()

if __name__ == '__main__':
    main()