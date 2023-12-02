"""
Maximum Flow Solution for Optimizing Air Canada Travel Routes

This program uses the Edmonds-Karp algorithm for finding the maximum flow in a flow network with the addition of
negative weights. The graph represents a city network with direct flights and constraints on the optimal route. The
maximum cost flow is calculated considering the given constraints, and the optimal route is determined using depth-first
search (DFS) in two rounds.

(1) Input Format:
The first line of input consists of two integers separated by a space, representing the number of vertices in the
airline graph (n) and the number of edges (m).

The next (n+1) lines contain one string each. The string on the (i+1)-th line represents the name of the city i from
west to east.

The following (m) lines contain two strings each, x and y, representing the existence of a direct flight route between
city x and city y.

(2) Output Format:

If a route exists, the output format is as follows:

Output an integer k on the first line, representing the maximum number of cities in the route.

From line 2 to (k+2), each line contains a string. The string on the (i+1)-th line represents the name of the i-th city
visited in the travel route. Note that the first and k-th cities are the departure and destination cities, respectively.

If no solution exists, output the string "No Solution!" on a single line.

(3) Sample Input:

8 9
Vancouver
Yellowknife
Edmonton
Calgary
Winnipeg
Toronto
Montreal
Halifax
Vancouver Edmonton
Vancouver Calgary
Calgary Winnipeg
Winnipeg Toronto
Toronto Halifax
Montreal Halifax
Edmonton Montreal
Edmonton Yellowknife
Edmonton Calgary

(4) Sample Output:

7
Vancouver
Calgary
Winnipeg
Toronto
Halifax
Montreal
Edmonton
Vancouver

"""

from collections import deque

"""
Constants:
- N: Maximum number of vertices in the graph.
- M: Maximum number of edges in the graph.
- INF: Represents infinity, a large value used for initialization.
"""
N = 103
M = 40000
INF = float('inf')

class FlowEdge:
    """
    Represents a directed edge in a flow network.

    Attributes:
    - weight (int): The weight or capacity of the edge.
    - destination (int): The destination vertex of the edge.
    - next_edge (int): The index of the next edge in the adjacency list.
    - flow (int): The current flow through the edge.
    """

    def __init__(self, weight, destination, next_edge, flow):
        """
        Initializes a new FlowEdge with the given attributes.

        Parameters:
        - weight (int): The weight or capacity of the edge.
        - destination (int): The destination vertex of the edge.
        - next_edge (int): The index of the next edge in the adjacency list.
        - flow (int): The current flow through the edge.
        """
        self.weight = weight
        self.destination = destination
        self.next_edge = next_edge
        self.flow = flow

def add_edge(start, end, capacity, weight):
    """
    Add an edge to the graph.

    Parameters:
    - start: Starting vertex of the edge.
    - end: Ending vertex of the edge.
    - capacity: Capacity of the edge.
    - weight: Weight or cost associated with the edge.

    Note: This function assumes a global array `flow_edges`, `head`, and `edge_index`.
    """
    global edge_index
    edge_index += 1
    flow_edges[edge_index] = FlowEdge(weight, end, head[start], capacity)
    head[start] = edge_index

def add_directed_edge(a, b, flow, weight):
    """
    Add a directed edge and its reverse edge to the graph.

    Parameters:
    - a: Starting vertex of the directed edge.
    - b: Ending vertex of the directed edge.
    - flow: Capacity of the directed edge.
    - weight: Weight or cost associated with the directed edge.

    Note: This function assumes a global array `flow_edges`, `head`, and `edge_index`.
    """
    global edge_index

    # Add the edge from a to b
    add_edge(a, b, flow, weight)

    # Add the reverse edge from b to a with capacity 0 and negative weight
    add_edge(b, a, 0, -weight)

def spfa(start, end):
    """
    SPFA (Shortest Path Faster Algorithm) for finding the shortest path in a graph with negative weights.

    Parameters:
    - start: Starting vertex of the path.
    - end: Ending vertex of the path.

    Returns:
    - True if there is a path from start to end, False otherwise.

    Note: This function assumes global arrays `distances`, `in_queue`, `min_residual_flow`, `head`, `predecessors`, and `flow_edges`.
    """
    global distances, in_queue, min_residual_flow

    # Initialize arrays for distances, in_queue flags, and minimum residual flow
    distances = [-INF] * (end + 1)
    in_queue = [0] * (end + 1)
    min_residual_flow = [0] * (end + 1)

    # Initialize a deque for the SPFA algorithm
    queue = deque()
    queue.append(start)
    in_queue[start] = 1
    distances[start] = 0
    min_residual_flow[start] = INF

    # SPFA Algorithm
    while queue:
        current = queue.popleft()
        in_queue[current] = 0

        # Iterate through outgoing edges from the current vertex
        edge_index = head[current]
        while edge_index:
            destination = flow_edges[edge_index].destination

            # Relaxation step
            if flow_edges[edge_index].flow and distances[destination] < distances[current] + flow_edges[edge_index].weight:
                distances[destination] = distances[current] + flow_edges[edge_index].weight
                predecessors[destination] = edge_index
                min_residual_flow[destination] = min(min_residual_flow[current], flow_edges[edge_index].flow)

                # Enqueue the destination vertex if not in the queue
                if not in_queue[destination]:
                    in_queue[destination] = 1
                    queue.append(destination)

            edge_index = flow_edges[edge_index].next_edge

    # Return True if there is a path from start to end, False otherwise
    return distances[end] != -INF

def edmonds_karp(start, end):
    """
    Edmonds-Karp algorithm for finding the maximum flow in a flow network.

    Parameters:
    - start: Source vertex of the flow network.
    - end: Sink vertex of the flow network.

    Note: This function assumes global variables `max_flow`, `max_cost`, `spfa`, `min_residual_flow`, `distances`, `predecessors`, and `flow_edges`.
    """
    global max_flow, max_cost

    # Iterate while there is an augmenting path
    while spfa(start, end):
        current = end

        # Update max flow and cost along the augmenting path
        max_flow += min_residual_flow[end]
        max_cost += min_residual_flow[end] * distances[end]

        # Update flow along the augmenting path
        while current != start:
            edge_index = predecessors[current]
            flow_edges[edge_index].flow -= min_residual_flow[end]
            flow_edges[edge_index ^ 1].flow += min_residual_flow[end]
            current = flow_edges[edge_index ^ 1].destination

def dfs_first_round(current):
    """
    DFS traversal in the first round to find the cities in the optimal route.

    Parameters:
    - current: Current vertex in the traversal.

    Note: This function assumes the global variable `visited`.
    """
    global visited

    # Mark the current node as visited
    visited[current] = 1

    # Print the city name associated with the current node
    print(city_names[current - n])

    # Traverse outgoing edges to find the next city in the path
    edge_index = head[current]
    while edge_index:
        destination = flow_edges[edge_index].destination
        if destination <= n and not flow_edges[edge_index].flow:
            # Recursively traverse to the next city
            dfs_first_round(destination + n)
            break

        # Move to the next edge
        edge_index = flow_edges[edge_index].next_edge

def dfs_second_round(current):
    """
    DFS traversal in the second round to find the cities in the optimal route.

    Parameters:
    - current: Current vertex in the traversal.

    Note: This function assumes the global variable `visited`.
    """
    global visited

    # Traverse outgoing edges to find the next city in the path
    edge_index = head[current]
    while edge_index:
        destination = flow_edges[edge_index].destination
        if destination <= n and not flow_edges[edge_index].flow and not visited[destination + n]:
            # Recursively traverse to the next city
            dfs_second_round(destination + n)
        edge_index = flow_edges[edge_index].next_edge

    # Print the city name associated with the current node (second round)
    print(city_names[current - n])

def main():
    global n, m, source, sink, flow_edges, head, distances, visited, predecessors, min_residual_flow, max_cost, max_flow, flag, city_names, city_mapping, edge_index

    try:
        # Read input values for the number of vertices (n) and the number of edges (m)
        n, m = map(int, input().split())

        edge_index = 1
        source = 1
        sink = n * 2
        flow_edges = [FlowEdge(0, 0, 0, 0) for _ in range(M << 1)]
        head = [0] * (N)
        distances = [0] * (N)
        visited =  [0] * (N)
        predecessors = [0] * (N)
        min_residual_flow = [0] * (N)
        max_cost = 0
        max_flow = 0
        flag = 0

        city_names = [""] * (N)
        city_mapping = {}

        # Read city names
        # print("Enter the names of cities (one city per line, in order form west to east):")
        for i in range(1, n + 1):
            city_names[i] = input()
            city_mapping[city_names[i]] = i

        for i in range(2, n):
            add_directed_edge(i, n + i, 1, 1)

        add_directed_edge(1, 1 + n, 2, 1)
        add_directed_edge(n, n + n, 2, 1)

        # Read direct flight routes
        # print("Enter direct flight routes (one filght route per line, city1 city2):")
        for _ in range(m):
            input_line = input().split()
            x = city_mapping[input_line[0]]
            y = city_mapping[input_line[1]]

            if x > y:
                x, y = y, x

            flag |= x == 1 and y == n
            add_directed_edge(x + n, y, 1, 0)

        # Execute the Edmonds-Karp algorithm
        edmonds_karp(source, sink)

        # Output result
        if max_flow == 2:
            print(max_cost - 2)
        elif max_flow == 1 and flag:
            print("2")
            print(city_names[1])
            print(city_names[n])
            print(city_names[1])
            return
        else:
            print("No Solution!")
            return

        # Execute DFS
        visited = [0] * (N * 2 + 1)

        dfs_first_round(1 + n)
        dfs_second_round(1 + n)

    except ValueError:
        print("Invalid input. Please enter valid integers for the number of cities and flights.")
    except KeyError:
        print("Invalid city name. Please enter valid city names.")
    except Exception as e:
        print("An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
