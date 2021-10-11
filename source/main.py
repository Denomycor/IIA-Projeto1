from searchPlus import (
    Problem, astar_search
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
    def __init__(self, size, blacks, white):
        #Size of the board
        self.size = size
        #List of the coordinates of all black pieces
        self.blacks = blacks
        #white coordinates
        self.white = white

    def clone(self):
        return PuzzleRobotsState(self.size, list(self.blacks), self.white)

    def display(self):
        bar = ['_']*self.size
        for row in range(self.size):
            print(bar)
            for col in range(self.size):
                coords = (col, 4-row)
                cont = ''
                if col == row and col == self.size//2 : 
                    cont = 'X'
                elif coords in self.blacks: 
                    cont = 'B'
                elif coords == self.white: 
                    cont = 'W'
                print('| '+cont+' |')
            print(bar)

    def __eq__(self, obj):
        return isinstance(obj, PuzzleRobotsState) and self.size == obj.size and \
            self.white == obj.white and self.blacks == obj.blacks

    def __ne__(self, obj):
        return not self == obj

class PuzzleRobotsAction:
    def __init__(self, moving, stop):
        #Coordinates of the moving piece
        self.moving = moving
        #Coordinates of the piece stoping the movement
        self.stop = stop
        #Final Position
        self.final_pos = ()

    def display(self):
        print("from: " + str(self.moving[0])+", "+str(self.moving[1])+" collinding with "+str(self.stop[0])+", "+str(self.stop[1]))

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

    """Get the cost of the action"""
    def actionCost(self):
        return abs(list(filter(lambda i: i != 0, tupleSub(self.moving, self.getFinalPos())))[0])


class PuzzleRobots(Problem):

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        for l in range(2):
            for i in range(state.size):
                col = [c for c in state.blacks + [state.white] if c[l] == i]
                col.sort()
                for a in range(len(col)):
                    if a != len(col)-1:
                        yield PuzzleRobotsAction(col[a], col[a+1])
                    if a != 0:
                        yield PuzzleRobotsAction(col[a], col[a-1])

    def result(self, state, action):
        new_state = state.clone()
        if(new_state.white == action.moving):
            new_state.white = action.getFinalPos()
        else:
            for i in range(len(new_state.blacks)):
                if(new_state.blacks[i] == action.moving):
                    new_state.blacks[i] = action.getFinalPos()
                    break
        return new_state
            
    def goal_test(self, state):
        return self.goal == state.white

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + action.actionCost()

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


class Solver:

    """Abstract framework for a problem-solving agent. [Figure 3.1]"""

    def __init__(self, initial_state=None):
        """State is an sbstract representation of the state
        of the world, and seq is the list of actions required
        to get to a particular state from the initial state(root)."""
        self.state = initial_state
        self.seq = []

    def __call__(self, percept):
        """[Figure 3.1] Formulate a goal and problem, then
        search for a sequence of actions to solve it."""
        self.state = self.update_state(self.state, percept)
        if not self.seq:
            goal = self.formulate_goal(self.state)
            problem = self.formulate_problem(self.state, goal)
            self.seq = self.search(problem)
            if not self.seq:
                return None
        return self.seq.pop(0)

    def update_state(self, percept):
        return percept.clone()

    def formulate_goal(self, state):
        return PuzzleRobotsState(state.size, state.blacks, (state.size//2,state.size//2))

    def formulate_problem(self, state, goal):
        return PuzzleRobots(state, goal)

    def search(self, problem):
        return astar_search(problem, ) 



#--TESTS ERASE ME LATER
init = PuzzleRobotsState(5, [(3,4), (0,2), (1,1), (3,1), (4,0)], (1,4))
prob = PuzzleRobots(init, (2,2))
i=0


for act in prob.actions(prob.initial):
    if i==0:
        new_state = prob.result(init, act)
        #print(act.actionCost())
        i+=1
    
    act.display()
    print(act.actionCost())
    print(act.getFinalPos())


#----
solver = Solver(init)

print(solver(init))

