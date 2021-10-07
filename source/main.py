
from enum import Enum
from source.utils import RIGHT
from searchPlus import (
    Problem
)

def tupleAdd(first, *others):
    temp = list(first)
    for tuple_ in others:
        for i in range(min(len(temp), len(tuple_))):
            temp[i] += tuple_[i]
    return tuple(temp)

def tupleSub(first, *others):
    temp = list(first)
    for tuple_ in others:
        for i in range(min(len(temp), len(tuple_))):
            temp[i] -= tuple_[i]
    return tuple(temp)
            

class PuzzleRobotsState:
    def __init__(self, size, blacks, white, curr_cost=0):
        #Size of the board
        self.size = size
        #List of the coordinates of all black pieces
        self.blacks = blacks
        #white coordinates
        self.white = white
        #Current cost
        self.curr_cost = curr_cost

    def clone(self):
        return PuzzleRobotsState(self.size, self.size, list(self.blacks), self.white, self.curr_cost)

class PuzzleRobotsAction:
    def __init__(self, moving, stop):
        #Coordinates of the moving piece
        self.moving = moving
        #Coordinates of the piece stoping the movement
        self.stop = stop
        #Final Position
        self.final_pos = ()

    """Get the final position of the piece, after the action"""
    def getFinalPos(self):
        if self.final_pos == ():
            if self.moving[0] == self.stop[0]:
                self.final_pos = (self.stop[0], self.stop[1] + (1 if self.stop[1] < self.moving[1] else -1))
            elif self.moving[1] == self.stop[1]:
                self.final_pos = (self.stop[0] + (1 if self.stop[0] < self.moving[0] else -1), self.stop[1])
            else:
                raise RuntimeError
        return self.final_pos

    def actionCost(self):
        return abs([i for i in tupleSub(self.moving - self.getFinalPos()) if i != 0][0])


class PuzzleRobots(Problem):

    def __init__(self, initial=PuzzleRobotsState(0), goal=None):
        self.initial = initial #Initial State
        self.goal = goal

    def actions(self, state):
        for l in range(2):
            for i in range(state.size):
                col = [c for c in state.blacks + state.white if c[l] == i].sort
                for a in range(len(col)-1):
                    if a != len(col)-2:
                        yield PuzzleRobotsAction(col[a], col[a+1])
                    elif a != 0:
                        yield PuzzleRobotsAction(col[a], col[a-1])

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError
            
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


