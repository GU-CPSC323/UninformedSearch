"""
Water Jug Problem
State representation:
    (x, y)

    x = amount of water in the 4-gallon jug
    y = amount of water in the 3-gallon jug
Actions:
    A = Fill 4-gallon jug
    B = Fill 3-gallon jug
    C = Empty 4-gallon jug
    D = Empty 3-gallon jug
    E = Pour 4-gallon jug into 3-gallon jug
    F = Pour 3-gallon jug into 4-gallon jug
"""
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

class WaterJugProblem:

    def __init__(self,initial_state):
        self.initial_state = initial_state

    def is_goal(self, state):
        """Return True if either jug contains exactly 2 gallons."""
        x, y = state
        return x == 2 or y == 2

    def successors(self, state):
        """Return legal successor states and their actions."""
        x, y = state
        children = []
        #A: Fill the 4-gallon jug
        if x < 4:
            children.append(((4, y), "A"))
        #B: Fill the 3-gallon jug
        if y < 3:
            children.append(((x, 3), "B"))
        #C: Empty the 4-gallon jug
        if x > 0:
            children.append(((0, y), "C"))
        #D: Empty the 3-gallon jug
        if y > 0:
            children.append(((x, 0), "D"))
        #E: Pour from 4-gallon jug into 3-gallon jug
        amount = min(x, 3 - y)
        if amount > 0:
            children.append(((x - amount, y + amount), "E"))
        #F: Pour from 3-gallon jug into 4-gallon jug
        amount = min(y, 4 - x)
        if amount > 0:
            children.append(((x + amount, y - amount), "F"))

        return children

#recontruct solution path
def get_solution(node):
    path = []
    actions = []
    #follow parent pointers back to the initial node
    while node is not None:
        path.append(node.state)
        if node.action is not None:
            actions.append(node.action)
        node = node.parent
    #we constructed the solution backwards
    path.reverse()
    actions.reverse()
    return path, actions


def graph_search(problem, strategy):
    """Perform graph search using BFS or DFS."""
    start = problem.initial_state
    frontier = [Node(start)]
    reached = {start}

    print ("Initial Frontier",[n.state for n in frontier])
    print("Initial Reached:", reached)

    while frontier:
        if strategy == "dfs":
            #LIFO
            node = frontier.pop()
        elif strategy == "bfs":
            #FIFO
            node = frontier.pop(0)
        else:
            print("not valid strategy")
            return

        print("\nExpanding:", node.state)

        #check for goal
        if problem.is_goal(node.state):
            return get_solution(node)

        #expand node
        children = problem.successors(node.state)
        print("Successors:", children)

        if strategy == "dfs":
            children.reverse()

        for child_state, action in children:
            if child_state not in reached:
                reached.add(child_state)
                child_node= Node(
                    child_state,
                    node,
                    action,
                    node.path_cost+1
                                 )
                frontier.append(child_node)
        print("Frontiers:", [(n.state, n.action) for n in frontier])
        print("Reached:", reached)
       

    return None, None

    

    
if __name__ == "__main__":

    #try "bfs" or "dfs"
    problem = WaterJugProblem((0,0))
    strategy = "dfs"
    path, actions = graph_search(problem, strategy)

    print("Path:", path)
    print("Actions:", actions)
    