import logging
import sqlite3
from sqlite3 import Error

class Store():
    
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error:
            logging.error("Cant't connect to database %s", db_file)

        return conn
    
    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return: True or None
        """
        success = None
        try:
            conn.execute(create_table_sql)
            success = True
        except Error:
            logging.error("Can't to execute %s", create_table_sql)
        
        return success
    
    def insert_data(self, conn, values):
        sql_insert = """INSERT INTO monitoring(date, energy, reactive_energy, power, maximeter, reactive_power, voltage, intensity, power_factor) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        with conn:
            conn.execute("DELETE FROM monitoring")
            conn.executemany(sql_insert, values)