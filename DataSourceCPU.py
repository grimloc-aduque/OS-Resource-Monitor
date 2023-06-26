
from time import time

import pandas as pd
import psutil

from DataSource import DataSource


class DataSourceCPU(DataSource):

    current_data:pd.Series
    historical:pd.DataFrame
    start_time:float

    def __init__(self):
        self.start_time = time()
        self.cpu_count = psutil.cpu_count()
        self.columns = [f"CPU{i}" for i in range(self.cpu_count)]
        self.historical = pd.DataFrame(columns=self.columns)
        self.historical.index.name = 'Time'

    def update_data(self):
        self.current_data = self._get_cpu_usage()
        self.current_data = pd.Series(self.current_data, index=self.columns)
        elapsed_time = time() - self.start_time
        self.historical.loc[elapsed_time] = self.current_data

    def get_data(self):
        return self.current_data

    def get_historical(self):
        return self.historical
    
    def save_file(self):
        self.historical.to_csv(f'{self.output_folder}/cpu_historical.csv')

    # System information

    def _get_cpu_count(self):
        return psutil.cpu_count()

    def _get_cpu_usage(self):
        return psutil.cpu_percent(percpu=True)
