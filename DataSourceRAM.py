
from time import time

import pandas as pd
import psutil

from DataSource import DataSource


class DataSourceRAM(DataSource):

    current_data:pd.Series
    historical:pd.DataFrame
    start_time:float

    def __init__(self):
        self.start_time = time()
        self.historical = pd.DataFrame(
            {
                "Used Memory": [],
                "Free Memory": [],
                "Used Swap": [],
                "Free Swap":[]
            })
        self.historical.index.name = 'Time'


    def update_data(self):
        self.current_data = pd.Series(
            {   
                "Used Memory": self._get_used_memory(),
                "Free Memory": self._get_available_memory(),
                "Used Swap": self._get_used_swap(),
                "Free Swap": self._get_free_swap()
            })
        elapsed_time = time() - self.start_time
        self.historical.loc[elapsed_time] = self.current_data


    def get_data(self):
        return self.current_data

    def get_historical(self):
        return self.historical

    def save_file(self):
        self.historical.to_csv(f'{self.output_folder}/ram_historical.csv')

    # System information

    def get_total_memory(self):
        return self.to_GB(psutil.virtual_memory()[0])

    def _get_available_memory(self):
        return self.to_GB(psutil.virtual_memory()[1])

    def _get_used_memory(self):
        return self.to_GB(psutil.virtual_memory()[3])
    
    def _get_used_swap(self):
        return self.to_GB(psutil.swap_memory()[1])
    
    def _get_free_swap(self):
        return self.to_GB(psutil.swap_memory()[2])









        