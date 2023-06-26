
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class DataSource(ABC):
    
    output_folder:str = './Data'

    def to_GB(self, bytes:int):
        return np.round(bytes/(10**9), 2)

    def to_KB(self, bytes:int):
        return np.round(bytes/(10**3), 2)

    @abstractmethod
    def update_data(self):
        pass

    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_historical(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def save_file(self):
        pass
