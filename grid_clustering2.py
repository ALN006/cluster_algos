#OOP approach
from cluster import *

def grid_cluster(k, points: cluster):

    """ assumes points is a cluster of 2d points and k is a integer
        
        divides the plane in which the points exist into k**2 rectangles which are stored in a list of rectangles
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
    
    minimum, maximum = points.range()
    span = maximum - minimum
    dimensions = span/k
    rectangles = {}

    index = (0.0,)*len(dimensions)
    while True:
        rectangles[index] = 0
        if index == (k-1,)*len(dimensions):
            break
        inde = NextBaseK(k,index)

    for point in points:
        rectangles[tuple(min((point - minimum)//dimensions), k-1)] += 1

    sorted_indexs = sorted([index for index in rectangles], key = lambda index: rectangles[index])

    decision_boundry = []

    for index in sorted_indexs:
        center = minimum + (np.array(index) + 0.5)*dimensions
        


def NextBaseK(k: int, prev_number: tuple) -> tuple:
    '''assumes prev_number is a tuple of digits that representts a number in base k'''
    for i in range(len(prev_number)):
        if prev_number[-i-1] < k -1:
            return prev_number[:-i-1] + (prev_number[-i-1]+1,) + (0,)*i

