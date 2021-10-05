
from enum import Enum
from source.utils import RIGHT
from searchPlus import (
    Problem
)

def tupleAdd(first, *others):
    temp = list(first)
    for tuple in others:
        for i in range(min(len(temp), len(tuple))):
            temp[i] += tuple[i]
    return temp

def tupleSub(first, *others):
    temp = list(first)
    for tuple in others:
        for i in range(min(len(temp), len(tuple))):
            temp[i] -= tuple[i]
    return temp
            
class Direction(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ERROR = 5

    @staticmethod
    def getDirectionList():
        return (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)

class PuzzleRobotsState:
    def __init__(self, size, blacks, white, curr_cost=0):
        #Size of the board
        self.size = size
        #Tuple of the coordinates of all black pieces
        self.black = blacks
        #white coordinates
        self.white = white
        #Current cost
        self.curr_cost = curr_cost

class PuzzleRobotsAction:
    def __init__(self, moving, stop, direction=Direction.NONE):
        #Coordinates of the moving piece
        self.moving = moving
        #Coordinates of the piece stoping the movement
        self.stop = stop
        #Direction of the movement
        self.direction = direction
        #Final Position
        self.final_pos = ()


    """Get the direction of the movement"""
    def getActionDirection(self):
        if(self.direction == Direction.NONE):
            if self.moving[0] == self.stop[0]:
                if self.moving[0] > self.stop[0]:
                    self.direction = Direction.LEFT
                elif self.moving[0] < self.stop[0]:
                    self.direction = Direction.RIGHT
            elif self.moving[1] == self.stop[1]:
                if self.moving[1] > self.stop[1]:
                    self.direction = Direction.DOWN
                elif self.moving[1] < self.stop[1]:
                    self.direction = Direction.UP
            else:
                self.direction = Direction.ERROR
        return self.direction

    """Get the final position of the piece, after the action"""
    def getFinalPos(self):
        if self.final_pos == ():
            self.final_pos = tupleAdd(self.stop, ((0,-1), (0,1), (1,0), (-1,0))[self.getActionDirection()-1])
        return self.final_pos

    def actionCost(self):
        return abs([i for i in tupleSub(self.moving - self.getFinalPos()) if i != 0][0])


class PuzzleRobots(Problem):

    def __init__(self, initial=PuzzleRobotsState(0), goal=None):
        self.initial = initial #Initial State
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        #Some invalid actions may occur when multiple pieces are on the same line
        #   o -> o -> o
        


    def result(self, state, action):
        if state.white == action.moving:
            state.white = action.getFinalPos()
            
            return state
        else:
            for

    def goal_test(self, state):
        return self.goal == state.white

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


