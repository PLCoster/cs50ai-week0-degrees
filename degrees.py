import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target, using BFS.

    source and target are unique IMDB actor ID's

    If no possible path, returns None.
    """

    # Initialise a QueueFrontier for BFS, with the starting actor ID:
    start = Node(source, None, None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialise an empty explored set to hold explored states (actors):
    explored = set()

    # Loop until a solution is found, or Frontier is empty(no solution):
    while True:

      if len(explored) % 100 == 0:
        print('Actors explored to find solution: ', len(explored))
        print('Nodes left to expand in Frontier: ', len(frontier.frontier))

      # Check for empty Frontier and return with no path if empty
      if frontier.empty():
        print('Frontier is Empty - No Connection Between Actors!')
        print(len(explored), 'actors explored to with no solution found!')
        return None

      # Otherwise expand the next node in the Queue, add it to the explored states and get set of movies and actors for the actor in the current node:
      curr_node = frontier.remove()
      explored.add(curr_node.state)

      for action, state in neighbors_for_person(curr_node.state):

        # If state (actor) is the target actor then solution has been found, return path:
        if state == target:
          print('Solution Found!')
          print(len(explored), 'actors explored to find solution!')
          # Create path from source to target
          path = []
          path.append((action, state))

          # Add action and state to path until back to start node
          while curr_node.parent != None:
            path.append((curr_node.action, curr_node.state))
            curr_node = curr_node.parent

          path.reverse()

          return path

        # Otherwise add the new states to explore to the frontier:
        if not frontier.contains_state(state) and state not in explored:
          new_node = Node(state, curr_node, action)
          frontier.add(new_node)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
