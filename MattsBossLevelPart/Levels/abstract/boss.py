from abc import ABC, abstractmethod

class Boss(ABC):

    @abstractmethod
    def getPosition():
        pass

    @abstractmethod
    def setPosition():
        pass

    @abstractmethod
    def drawBoss():
        pass