from mediator_game import Mediator
import sys

mediator = Mediator()

mediator.run1()

if (mediator.getPlayingStatus()==True):

    mediator.run2()

if (mediator.getPlayingStatus() == True):

    mediator.run3()

sys.exit()
