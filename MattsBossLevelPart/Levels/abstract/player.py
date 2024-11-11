from abc import ABC, abstractmethod

class Player(ABC):

    @abstractmethod
    def getPosition():
        pass

    @abstractmethod
    def updatePosition():
        pass

    @abstractmethod
    def drawPlayer():
        pass

    @abstractmethod
    def reduceHealth():
        pass
