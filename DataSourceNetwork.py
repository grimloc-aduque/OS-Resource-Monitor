
from time import time

import pandas as pd
import psutil

from DataSource import DataSource


class DataSourceNetwork(DataSource):

    previous_data:pd.Series
    current_data:pd.Series
    historical:pd.DataFrame
    start_time:float

    def __init__(self):
        self.current_data = None
        self.start_time = time()
        self.historical = pd.DataFrame(
            {
                "Bytes Sending": [],
                "Bytes Receiving":[]
            })
        self.historical.index.name = 'Time'
        

    def update_data(self):
        self.previous_data = self.current_data
        self.current_data = pd.Series(
            {
                "Bytes Sending": self._get_sent_bytes(),
                "Bytes Receiving": self._get_recv_bytes()
            })
        elapsed_time = time() - self.start_time
        self.historical.loc[elapsed_time] = self.current_data

    def get_data(self):
        if(len(self.historical) == 1):
            return pd.Series({"Bytes Sending": 0,"Bytes Receiving":0})
        return self.current_data - self.previous_data

    def get_historical(self):
        return self.historical

    def save_file(self):
        self.historical.to_csv(f'{self.output_folder}/network_historical.csv')

    # System information

    def _get_sent_bytes(self):
        return self.to_KB(psutil.net_io_counters()[0])
    
    def _get_recv_bytes(self):
        return self.to_KB(psutil.net_io_counters()[1])