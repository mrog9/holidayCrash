from abc import ABC, abstractmethod

class Player(ABC):

    @abstractmethod
    def getPosition():
        pass

    @abstractmethod
    def setPosition():
        pass

    @abstractmethod
    def drawPlayer():
        pass
