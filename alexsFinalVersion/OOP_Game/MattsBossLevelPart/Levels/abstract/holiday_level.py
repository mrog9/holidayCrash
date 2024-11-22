from abc import ABC, abstractmethod

class HolidayLevel(ABC):

    @abstractmethod
    def createBoss(self):
        pass
    
    @abstractmethod
    def createPlayer(self):
        pass

    @abstractmethod
    def createSetting(self):
        pass
        
    