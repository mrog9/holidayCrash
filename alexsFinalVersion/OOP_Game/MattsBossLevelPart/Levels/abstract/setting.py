from abc import ABC, abstractmethod

class Setting(ABC):

    @abstractmethod
    def getSetting():
        pass
