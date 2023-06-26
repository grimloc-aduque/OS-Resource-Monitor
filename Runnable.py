

from abc import ABC, abstractmethod
from time import sleep


class Runnable(ABC):

    is_running:bool
    sleep_time:int

    def __init__(self):
        self.is_running = False
        self.sleep_time = 1

    def run(self):
        sleep(2)
        self.is_running = True
        while True:
            if not self.is_running:
                break
            self.run_actions()
            sleep(self.sleep_time)
        print(f"Runnable Finished: {self.__class__}")

    @abstractmethod
    def run_actions():
        pass

