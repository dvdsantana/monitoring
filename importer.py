import logging
from store import Store
from csv_reader import CsvReader

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    db = Store()
    reader = CsvReader()
    
    data = reader.get_data_from_csv('Monitoring report.csv')
    if data is None:
        exit

    conn = db.create_connection(db_file='monitoring-report.db')
    if conn is None:
        exit

    # Create the monitoring table
    sql_create_table = "CREATE TABLE IF NOT EXISTS monitoring(date, energy, reactive_energy, power, maximeter, reactive_power, voltage, intensity, power_factor)"
    
    if db.create_table(conn, sql_create_table) is None:
        exit

    values = []
    for index, row in data.iterrows():
        values.append(row)

    db.insert_data(conn, values)

    conn.close()

if __name__ == '__main__':
    main()

