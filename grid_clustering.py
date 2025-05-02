#functional approcah

def grid_cluster(k, points):

    """ assumes points is a list of tuples of the form (x,y) representing points and k is a integer
        
        divides the plane in which the points exist into k**2 rectangles which are stored in a list rectangles
        models a rectangle a list of the form [<num points in rectangle>, <rectangle location>]
        
        sorts the rectangles by density/#points and stores the result in sorted_rectangles
        
        calculates the smallest chain of the least dense rectangles the divides the plane in 2
        returns result as a list of locations called decision_boundry which may be interprited as a line 

        this program is not stochastic, It will return the same decision boundry for the same data every time

        this program is effectively O(n) because k is genrally a small number(~5-500), 
        if k is large this program will be O(k**2*log(k))

        while this program is only for 2d data a version of this program with n-dimensional cuboids may be implemented similarly, 
        although its efficiancy suffers  in higher dimensions, becoming of the order O(n*log(k)*k**n) 

        the main advantage of this program is that it has no bias towards any particular cluster shape unlike a program lik KMeans say which
        heavily biases towards n-dimensioonal spheres.
        
        should be employed recusrsizely if more than 2 clusters are desired"""
    
    x_min = min(p[0] for p in points)
    y_min = min(p[1] for p in points)
    x_max = max(p[0] for p in points)
    y_max = max(p[1] for p in points)

    x_range = x_max - x_min
    y_range = y_max - y_min
    x_len = (x_range) / k
    y_len = (y_range) / k

    rectangles = [[[0] for _ in range(k)] for _ in range(k)] 
    for x, y in points:
        rectangles[min(int((y - y_min) // y_len), k - 1)][min(int((x - x_min) // x_len), k - 1)][0] += 1
    for y in range(k):
        for x in range(k):
            rectangles[y][x] += [(x_min + x * x_len + x_len / 2 , y_min + y * y_len + y_len / 2)]

    sorted_rectangles = sorted([rectangle for row in rectangles for rectangle in row], key = lambda r: r[0])

    decision_boundary = []
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    for _ , (x, y) in sorted_rectangles:
        decision_boundary.append((x, y))
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

        if (max_x - min_x >= x_range - x_len - 0.01) or (max_y - min_y >= y_range - y_len -0.01):
            break

    return decision_boundary

#example
import random
x_vals = [random.random()*100 for _ in range(100000)]
y_vals = [random.random()*100 for _ in range(100000)]
vals = list(zip(x_vals, y_vals))
print(grid_cluster(10, vals))