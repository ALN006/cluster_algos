import pylab
import numpy as np
import pandas as pd
import random
class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes"""

    def __init__(self, attributes = []):
        self.series = pd.Series(attributes)
    def __str__(self):
        return str(list(self.series))
    def __repr__(self):
        return str(list(self.series))
    def __eq__(self, other):
        return (self.series == other.series).all()
    
    def __add__(self, other):
        if isinstance(other, point):
            return point(self.series + other.series)
        else:
            return point(self.series + other)
    def __sub__(self, other):
        return self + other * -1
    def __mul__(self, other):
        if isinstance(other, point):
            return point(self.series * other.series)
        else:
            return point(self.series * other)
    def __pow__(self, other):
        if isinstance(other, point):
            return point(self.series ** other.series)
        else:
            return point(self.series ** other)
    
    def __len__(self):
        return len(self.series)
    def __getitem__(self, index):
        return self.series[index]
    def __setitem__(self, index, value):
        self.series[index] = value
    def __iter__(self): 
        return iter(self.series)
    def __contains__(self, item): 
        return item in self.series.values
    
    def length(self):
        return self.euclidean_distance(point([0]*len(self.series)))
    def manhattan_distance(self, other):
        return sum(abs(self.series - other.series))
    def euclidean_distance(self, other):
        return sum((self.series - other.series)**2)**0.5
    def dot(self, other):
        return sum(self.series * other.series)
    
    def get_attributes(self):
        return list(self.series)
    def set_attributes(self, attributes):
        self.series = pd.Series(attributes)

class cluster(object): 
    """assumes self is a cluster of points, models self as a list of point objects"""
    def __init__(self, points = []):
        self.points = points
        self.df = pd.DataFrame([p.get_attributes() for p in points])
    def __str__(self):
        return str(self.df)
    def __eq__(self, other):
        return (self.df == other.df).all().all()
    def __repr__(self):
        return str(self.df)
    def __add__(self, other):
        return cluster(self.points + other.points)
    def __sub__(self, other):
        """returns a new cluster with all points in self that are not in other"""
        return cluster([p for p in self.points if p not in other.points])
    
    def centroid(self):
        """returns the centroid of self as a point object"""
        return point([sum(self.df[i])/len(self.df) for i in range(len(self.df))])
    def intensive_linkage(self, other,link = "single", distance_function = point.euclidean_distance):
        """returns linkage vector between self and other"""
        link_f = {"single": (lambda x,y: x < y), "complete": (lambda x,y: x > y)}
        d = distance_function(self.df.loc[0],other.df.loc[0])
        ans = self.df.loc[0] - other.df.loc[0]
        for i in range(len(self.df)):
            for j in range(len(other.df)):
                distance = distance_function(self.df.loc[i],other.df.loc[j])
                if link_f[link](distance, d):
                    d = distance
                    ans = self.df.loc[i] - other.df.loc[j]
        return point(ans)
    def centroid_linkage(self, other):
        return (self.centroid() - other.centroid())
    def scaled(self, scalar):
        return cluster([self.df.loc[i]*scalar for i in range(len(self))])#this should work
    
    def get_df(self):
        return self.df
    
    def append(self, point):
        self.points.append(point)
    def remove(self, point):
        self.points.remove(point)
    def clear(self):
        self.points = []
    def normalized(self):
        points = self.points.copy()
        mins = points[0].get_attributes()
        maxs = points[0].get_attributes()
        n = len(points[0])
        for p in points:
            for i in range(n):
                if p.attribute(i) < mins[i]:
                    mins[i] = p.attribute(i)
                if p.attribute(i) > maxs[i]:
                    maxs[i] = p.attribute(i)
        for p in points:
            p.set_attributes((p.get_attributes() - mins) / (maxs - mins))
        return cluster(points)

class test_point(object):
    
    def __init__(self, trials, dimensions):
        self.dimensions = dimensions
        self.trials = trials

    def add(self):
        '''tests __add__,__sub__,__init__,__eq__,__repr,__str__'''
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if point((p1 + p2).get_attributes()) != point(pylab.array(L1) + pylab.array(L2)):
                print(f"add failed\n p1 = {p1}\n p2 = {p2}\n p1 + p2 = {p1 + p2}")
                return False
        return True
    def mul(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if (p1 * p2) != point(pylab.array(L1) * pylab.array(L2)):
                print(f"mul failed\n p1 = {p1}\n p2 = {p2}\n p1 * p2 = {p1 * p2}")
                return False
        return True
    def len(self):
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point(L)
            if len(p) != len(L):
                print(f"len failed\n p = {p}\n len(p) = {len(p)}\n len(L) = {len(L)}")
                return False
        return True
    def manhattan_distance(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if p1.manhattan_distance(p2) != sum(abs(pylab.array(L1) - pylab.array(L2))):
                print(f"manhattan_distance failed\n p1 = {p1}\n p2 = {p2}\n p1.manhattan_distance(p2) = {p1.manhattan_distance(p2)}")
                return False
        return True
    def euclidean_distance(self):
        for i in range(self.trials):
            L1 = [random.random() for j in range(self.dimensions)]
            L2 = [random.random() for j in range(self.dimensions)]
            p1 = point(L1)
            p2 = point(L2)
            if p1.euclidean_distance(p2) != sum((p1 - p2)**2)**0.5:
                print(f"euclidean_distance failed\n p1 = {p1}\n p2 = {p2}\n p1.euclidean_distance(p2) = {p1.euclidean_distance(p2)}")
                return False
        return True
    def assignment(self):
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point()
            p.set_attributes(L)
            x = p[0]
            p[0] = x + 1
            L[0] = x + 1
            if p[0] == x or p[0] != x + 1 or p.get_attributes() != L:
                print(f"item_assignment failed\n p = {p}\n intial val of p[0] -> x = {x}\n final value is not incremented by 1 -> p[0] = {p[0]}")
                return False
        return True
    def iteration(self): 
        for i in range(self.trials):
            L = [random.random() for j in range(self.dimensions)]
            p = point(L)
            for k in p:
                if k not in p:
                    print(f"iteration failed\n p = {p}\n k = {k}\n k not in p = {k not in p}")
                    return False
        return True
 
    def TestAll(self):
        result = True
        tests = [self.add, self.mul, self.len, self.manhattan_distance, self.euclidean_distance, self.assignment, self.iteration]
        for t in tests:
            if not t():
                result = False
        return result
