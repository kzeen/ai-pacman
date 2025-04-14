# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    # The frontier is implemented as a stack for DFS (LIFO)
    frontier = Stack()
    # The visited set is implemented as a set to make sure we don't visit the same state twice (unique entries)
    visited = set()

    startState = problem.getStartState()
    # Push to stack a tuple of (state, pathToGetThere)
    frontier.push((startState, []))

    while not frontier.isEmpty():
        # Pop last inserted state-path tuple
        currState, currPath = frontier.pop()

        # If current state is the goal state, return the path
        if problem.isGoalState(currState):
            return currPath
        
        # If state has not been visited, expand it
        if currState not in visited:
            visited.add(currState)
            # Loop through all successors of current state
            for successor, action, stepCost in problem.getSuccessors(currState):
                # But only consider those that are not yet visited
                if successor not in visited:
                    # Append action to path to reach this successor
                    newPath = currPath + [action]
                    frontier.push((successor, newPath))
            
    # Return an empty list (no actions) if no solution is found
    return []

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    # The frontier is now implemented as a queue for BFS (FIFO)
    frontier = Queue()
    visited = set()

    startState = problem.getStartState()
    frontier.push((startState, [])) # (state, pathToGetThere)

    while not frontier.isEmpty():
        # Pop the earliest-inserted tuple
        currState, currPath = frontier.pop()

        if problem.isGoalState(currState):
            return currPath
        
        if currState not in visited:
            visited.add(currState)

            for successor, action, stepCost in problem.getSuccessors(currState):
                if successor not in visited:
                    newPath = currPath + [action]
                    frontier.push((successor, newPath))

    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # The frontier is now implemented as a priority queue where lowest total cost nodes are expanded first
    frontier = PriorityQueue()
    # visited is now a dictionary that maps states to their lowest/best known cost to reach them so far
    visited = {}

    startState = problem.getStartState()
    frontier.push((startState, []), 0) # ((state, pathToGetThere), cumulativeCost)

    while not frontier.isEmpty():
        currState, currPath = frontier.pop() # PriorityQueue pop() only returns tuple "item"

        if problem.isGoalState(currState):
            return currPath
        
        # Get the cumulative cost needed to reach the current state
        costSoFar = problem.getCostOfActions(currPath)
        # Expand the state if it has not been visited or if it has a lower cost than the previous path to this state
        if currState not in visited or costSoFar < visited[currState]:
            visited[currState] = costSoFar

            for successor, action, stepCost in problem.getSuccessors(currState):
                newPath = currPath + [action]
                newCost = problem.getCostOfActions(newPath)
                if successor not in visited or newCost < visited[successor]:
                    frontier.push((successor, newPath), newCost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    # Also uses a priority queue but is now ordered by pathCost + heuristic
    frontier = PriorityQueue()
    visited = {} 

    startState = problem.getStartState()
    # The priority = pathCost + heuristic
    startCost = 0 + heuristic(startState, problem)
    frontier.push((startState, []), startCost) # ((state, PathToGetThere), cumulativeCost + heuristic)

    while not frontier.isEmpty():
        currState, currPath = frontier.pop()

        if problem.isGoalState(currState):
            return currPath
        
        costSoFar = problem.getCostOfActions(currPath)
        if currState not in visited or costSoFar < visited[currState]:
            visited[currState] = costSoFar

            for successor, action, stepCost in problem.getSuccessors(currState):
                newPath = currPath + [action]
                newCost = problem.getCostOfActions(newPath)
                priority = newCost + heuristic(successor, problem)
                if successor not in visited or newCost < visited[successor]:
                    frontier.push((successor, newPath), priority)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
