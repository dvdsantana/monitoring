import pandas as pd
import logging

class CsvReader():
    def get_data_from_csv(self, csv_file):
        """ read a csv file specified by csv_file
        :param csv_file: csv file
        :return: Dataframe object or None
        """
        data = None
        try:
            column_names = ['date', 'energy', 'reactive_energy', 'power', 'maximeter', 'reactive_power', 'voltage', 'intensity', 'power_factor']
            data = pd.read_csv('Monitoring report.csv', names=column_names, skiprows=1)
            return data
        except:
            logging.error("Can't read csv file %s. Check if the file exists and it's well formed", csv_file)
        
        return data
