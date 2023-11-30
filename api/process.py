"""
Dynamic Programming Solution for Optimizing Air Canada Travel Routes

In this dynamic programming solution, dp[i][j] represents the state where two travelers are at cities i and j
respectively, and they only move to cities with numbers greater than max(i, j).

The idea is to ensure that at each step, the travelers move towards the rightmost city beyond their current positions.
Even if there are intermediate states such as (i+1, j), they can be reached from (i, j) by transitioning through
states like (i+1, j-x).

The algorithm simulates the process where two travelers, starting simultaneously from the initial city, move towards
the rightmost city. The dynamic programming values are updated based on the maximum number of cities visited by both
travelers.

Note: Variables x and y in the program represent the city indices visited by the two travelers.

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
Edmonton
Montreal
Halifax
Toronto
Winnipeg
Calgary
Vancouver

"""

"""
Constants:
- INF: Represents infinity in the context of the algorithm.
- N: Maximum number of vertices in the graph.
"""
INF = float('inf')
N = 103

def find_optimal_routes(x, y):
    """
    Find the optimal number of routes from city x to city y using dynamic programming.

    Parameters:
    - x: Current city index for the first traveler.
    - y: Current city index for the second traveler.

    Returns:
    - The optimal number of routes from city x to city y.

    Note: This function assumes global variables `dp` and `road`, where dp[i][j] represents the state where
    two travelers are at cities i and j respectively, and they only move to cities with numbers greater than max(i, j).
    """
    global dp, road

    # Check if the dynamic programming value for the current point is already calculated
    if dp[x][y]:
        return dp[x][y]

    # Check if the sum of x and y is 1 (reached the starting point)
    if x + y == 1:
        return 0

    # Determine the minimum of x and y
    mm = min(x, y)

    # Iterate through the range of mm
    for i in range(mm):
        # Check if there is a road connecting the current city to the i-th city from the second traveler's route
        if road[i][x]:
            # Update the dynamic programming values for the current and target cities
            dp[y][x] = dp[x][y] = max(dp[x][y], find_optimal_routes(i, y) + 1)

        # Check if there is a road connecting the current city to the i-th city from the first traveler's route
        if road[i][y]:
            # Update the dynamic programming values for the current and target cities
            dp[y][x] = dp[x][y] = max(dp[x][y], find_optimal_routes(i, x) + 1)

    # Check if the dynamic programming value for the current point is still not updated
    if not dp[x][y]:
        return -INF

    # Return the dynamic programming value for the current point
    return dp[x][y]

"""
- total_points: Total number of points visited during the route optimization process
- points_from_x: List to store points reachable from the current city for the first traveler.
- points_from_y: List to store points reachable from the current city for the second traveler.
"""
total_points = 0
points_from_x = [0] * (N * N)
points_from_y = [0] * (N * N)

def find_solution(x, y):
    """
    Recursively finds the optimal route by backtracking from the end to the starting point.

    Parameters:
    - x: Current city index for the first traveler.
    - y: Current city index for the second traveler.
    """
    global total_points

    # Initialize the list to store the travel route
    travel_route = []

    # Increase the total_points count
    total_points += 1

    # Store the city index of the current point for the first traveler
    points_from_x[total_points] = x

    # Store the city index of the current point for the second traveler
    points_from_y[total_points] = y

    # Check if the sum of x and y is 1 (reached the starting point)
    if x + y == 1:
        return

    # Determine the minimum of x and y
    mm = min(x, y)

    # Iterate through the range of mm
    for i in range(mm):
        # Check if the dp value of the current city for the first traveler is one less than the dp value of the target
        # city, and there is a road connecting these cities
        if dp[i][y] == dp[x][y] - 1 and road[i][x]:
            # Recursively call the function for the next point
            find_solution(i, y)
            return

        # Check if the dp value of the current city for the second traveler is one less than the dp value of the target
        # city, and there is a road connecting these cities
        if dp[x][i] == dp[x][y] - 1 and road[i][y]:
            # Recursively call the function for the next point
            find_solution(x, i)
            return

def main():
    global n, m, cities, city_indices, road, dp, points_from_x, points_from_y

    try:
        # Read input values for the number of cities (n) and the number of flights (m)
        n, m = map(int, input().split())

        cities = {}
        city_indices = {}
        road = [[0] * (n + 1) for _ in range(n + 1)]
        dp = [[0] * (n + 1) for _ in range(n + 1)]

        # Read city names
        for i in range(1, n + 1):
            city_name = input()
            cities[i] = city_name
            city_indices[city_name] = i

        # Read direct flight routes
        for i in range(1, m + 1):
            input_line = input().split()
            x, y = city_indices[input_line[0]], city_indices[input_line[1]]
            road[x][y] = road[y][x] = 1
            if x == 1:
                road[0][y] = road[y][0] = 1
            elif y == 1:
                road[0][x] = road[x][0] = 1

        find_optimal_routes(n, n)

        # Check if there is a valid solution, if not, print an error message and return
        if not dp[n][n]:
            print("No Solution!")
            return

        # Print the maximum value of the dynamic programming table
        print(dp[n][n])

        for i in range(1, n):
            # Check if the current position has a value one less than the maximum in the last column
            if dp[i][n] == dp[n][n] - 1:
                find_solution(i, n)
                break

        # Remove duplicates from the list of points_from_x and sort it
        points_from_x = sorted(set(points_from_x[1:total_points + 1]))

        # Remove duplicates from the list of points_from_y and sort it
        points_from_y = sorted(set(points_from_y[1:total_points + 1]))

        sz1 = len(points_from_x)
        sz2 = len(points_from_y)

        # Print the starting city
        print(cities[1])

        # Iterate through the range of 1 to sz1
        for i in range(1, sz1):
            # Check if the current city index for the first traveler is greater than 1
            if points_from_x[i] > 1:
                # Print the city corresponding to the current city index for the first traveler
                print(cities[points_from_x[i]])

        # Iterate in reverse through the range of sz2 - 1 to 0
        for i in range(sz2 - 1, 0, -1):
            # Check if the current city index for the second traveler is greater than 1
            if points_from_y[i] > 1:
                # Print the city corresponding to the current city index for the second traveler
                print(cities[points_from_y[i]])

        # Print the starting city again to complete the cycle
        print(cities[1])

        return

    except ValueError:
        print("Invalid input. Please enter valid integers for the number of cities and flights.")
    except KeyError:
        print("Invalid city name. Please enter valid city names.")
    except Exception as e:
        print("An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
