class Node():
  """ Node class that represents a state, its parent state and the action that when applied to the parent resulted in this state """

  def __init__(self, state, parent, action):
    self.state = state
    self.parent = parent
    self.action = action


class StackFrontier():
  """ Stack Frontier Class that represents states to be expanded during the search. The stack frontier uses a last-in first out ordering to determine the next state to expand when searching for solutions. This results in a Depth-First Search type algorithm """

  def __init__(self):
    self.frontier = []

  def add(self, node):
    self.frontier.append(node)

  def contains_state(self, state):
    return any(node.state == state for node in self.frontier)

  def empty(self):
    return len(self.frontier) == 0

  def remove(self):
    if self.empty():
      raise Exception("empty frontier")
    else:
      node = self.frontier[-1]
      self.frontier = self.frontier[:-1]
      return node


class QueueFrontier(StackFrontier):
  """ Queue Frontier Class, which extends the StackFrontier class. It uses a first-in first-out ordering to determine the next state to expand when searching for solutions. This results in a Breadth-First Search type algorithm """

  def remove(self):
    if self.empty():
      raise Exception("empty frontier")
    else:
      node = self.frontier[0]
      self.frontier = self.frontier[1:]
      return node
