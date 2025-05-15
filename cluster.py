import pandas as pd
import numpy as np
import unittest     
import random  

from point import point
from matplotlib import pyplot as plt

class cluster(object):
    
    '''assumes self is a cluster of points, models self as a list of point objects'''

    def __init__(self,data:list[point]):
        if isinstance(data, pd.DataFrame):
            self.points = list(point(x) for x in data.values.tolist())
        else: 
            self.points = data
    def __eq__(self,other):
        return set(self.points) == set(other.points) 
    def __repr__(self):
        return str(self.points)
    def __len__(self):
        return len(self.points)
    def __hash__(self):
        return hash(tuple(hash(p) for p in self.points))

    def arithematic(self,other, operation):
        ''' returns a new cluster as the result of element wise operation of first n elements of self and other where n = len'''
        if isinstance(other,cluster):
            return cluster([ operation(a,b) for a,b in zip(self.points,other.points)])
        elif isinstance(other,list):
            return cluster([ operation(a,b) for a,b in zip(self.points,other)])
        else:
            return cluster([ operation(p,other) for p in self.points])
    def __add__(self,other):
        return cluster.arithematic(self,other, lambda x,y: x + y)
    def __sub__(self,other):
        return cluster.arithematic(self,other, lambda x,y: x - y)
    def __mul__(self,other):
        return cluster.arithematic(self,other, lambda x,y: x * y)
    def __truediv__(self,other):
        return cluster.arithematic(self,other, lambda x,y: x / y)
    def __pow__(self,other):
        return cluster.arithematic(self,other, lambda x,y: x ** y)

    def __getitem__(self, index):
        return self.points[index]
    def __setitem__(self, index, item):
        self.points[index] = item
    def __iter__(self):
        return iter(self.points)
    def __contains__(self, point):
        return point in self.points
    
    def distance_matrix(self,other, f = point.euclidean_distance):
        L =[]
        for i in self.points:
            row =[]
            for j in other.points:
                row += [f(i,j)]
            L += [row]
        return L
    def centroid(self):
        a = point([0]*len(self.points[0]))
        for i in self.points:
            a += i
        return a/len(self.points)
    def centroid_linkage(self,other, f = point.euclidean_distance):
        return f(self.centroid(), other.centroid())
    def single_linkage(self,other, f = point.euclidean_distance):
        return min([min(i) for i in cluster.distance_matrix(self,other, f)])
    def complete_linkage(self,other, f = point.euclidean_distance):
        return max([max(i) for i in cluster.distance_matrix(self,other, f)])
    def range(self):
        minimum = np.array(self.points[0])
        maximum = np.array(self.points[0])
        for i in self.points:
            for j in range(len(self.points[0])):
                if i[j] < minimum[j]:
                    minimum[j] = i[j]
                if i[j] > maximum[j]:
                    maximum[j] = i[j]
        return minimum, maximum
    def normalized(self):
        minimum, maximum = self.range()
        if (minimum == maximum).all(): 
            return cluster([point([1]*len(maximum)) for _ in self.points])
        else:
            return cluster([(p - minimum)/(maximum-minimum) for p in self.points])
    def merged(self, other):
        return cluster(self.points + other.points)
    def copy(self):
        return cluster([p.copy() for p in self.points])
    
    def plot(self: "cluster", c: str = "blue", attributes: list = [0,1]) -> None:
        for point in self.points:
            point.plot(color = c, components = attributes)
    
    def get_points(self):
        return self.points
    def set_points(self, points):
        self.points = points
    def append(self,point):
        self.points += [point]
    
class test_cluster(unittest.TestCase):
    '''self is a sorted list of random points used to test class cluster'''

    def setUp(self):
        self.clusters = [point([random.random() for _ in range(3)]) for _ in range(100)]
    def test_eq(self):
        for i in range(0,len(self.clusters)-1,10):
            self.assertEqual(cluster(self.clusters[i:i+10]),cluster(self.clusters[i:i+10]))
            self.assertNotEqual(cluster(self.clusters[i:i+9]),cluster(self.clusters[i:i+10]))
            self.assertNotEqual(cluster(self.clusters[i+1:i+11]),cluster(self.clusters[i:i+10]))
    def test_string(self):
        for i in range(0,len(self.clusters),10):
            L = self.clusters[i:i+10]
            self.assertEqual(str(cluster(L)),str(L))
    def test_len(self):
        for i in range(0,len(self.clusters),10):
            self.assertEqual(len(self.clusters[i:i+10]), len(cluster(self.clusters[i:i+10])))
    def test_hash(self):
        for i in range(0,len(self.clusters),10):
            self.assertTrue(isinstance(hash(cluster(self.clusters[i:i+10])), int))
            self.assertNotEqual(hash(cluster(self.clusters[i:i+10])), hash(cluster(self.clusters[i+1:i+11])))
    
    def arithematic(self, op):
        for i in range(0,len(self.clusters),10):
            c = op(cluster(self.clusters[i:i+10]), cluster(self.clusters[i+1:i+11]))
            r = random.random()
            self.assertTrue(isinstance(c, cluster))
            self.assertEqual(c,cluster([op(a,b) for a,b in zip(self.clusters[i:i+10],self.clusters[i+1:i+11])]))
            self.assertTrue(isinstance(op(c,r), cluster))
            self.assertEqual(op(c,r), op(c,r) + 0.0000001)
    def test_add(self):
        test_cluster.arithematic(self, lambda x,y: x + y)
    def test_sub(self):
        test_cluster.arithematic(self, lambda x,y: x - y)
    def test_mul(self):
        test_cluster.arithematic(self, lambda x,y: x * y)
    def test_div(self):
        test_cluster.arithematic(self, lambda x,y: x / y)
    def test_pow(self):
        test_cluster.arithematic(self, lambda x,y: x ** y)
    
    def test_get_item(self):
        for i in range(0,len(self.clusters),10):
            self.assertEqual(cluster(self.clusters[i:i+10])[0],self.clusters[i:i+10][0])
    def test_set_item(self):
        for i in range(0,len(self.clusters),10):
            c = cluster(self.clusters[i:i+10])
            c[0] = 2
            self.assertEqual(c[0],2)
    def test_iter_contains(self):
        for i in range(0,len(self.clusters),10):
            c = cluster(self.clusters[i:i+10])
            for i in c:
                self.assertTrue(i in c)

    def test_centroid(self):
        for i in range(0,len(self.clusters),10):
            a = point([0]*3)
            for j in self.clusters[i:i+10]:
                a += j/len(self.clusters[i:i+10])
            self.assertTrue(isinstance(cluster(self.clusters[i:i+10]).centroid(),point))
            self.assertEqual(cluster(self.clusters[i:i+10]).centroid(), a)
    def test_centroid_linkage(self):
        for i in range(0,len(self.clusters),10):
           d = cluster.centroid_linkage(cluster(self.clusters[i:i+10]), cluster(self.clusters[i+5:i+15]))
           d2 = cluster.centroid_linkage(cluster(self.clusters[i:i+10]), cluster(self.clusters[i+5:i+15]), f = point.manhattan_distance)
           self.assertTrue(isinstance(d, float))
           self.assertEqual(d, sum((cluster(self.clusters[i:i+10]).centroid() - cluster(self.clusters[i+5:i+15]).centroid())**2)**0.5)
           self.assertEqual(d2, sum(abs(cluster(self.clusters[i:i+10]).centroid() - cluster(self.clusters[i+5:i+15]).centroid()))) 
    def test_dist_matrix(self):
        for i in range(0,len(self.clusters),10):
            matrix = cluster.distance_matrix(cluster(self.clusters[i:i+10]), cluster(self.clusters[i+5:i+15]))
            for j in range(len(matrix)):
                for k in range(len(matrix[0])):
                    self.assertEqual(matrix[j][k], self.clusters[i:i+10][j].euclidean_distance(self.clusters[i+5:i+15][k]))
    def test_single_linkage(self):
        for i in range(0,len(self.clusters),10):
            d = min([min(i) for i in cluster.distance_matrix(cluster(self.clusters[i:i+10]), cluster(self.clusters[0:10]))])
            self.assertEqual(d, cluster.single_linkage(cluster(self.clusters[i:i+10]), cluster(self.clusters[0:10])))
    def test_complete_linkage(self):
        for i in range(0,len(self.clusters),10):
            d = max([max(i) for i in cluster.distance_matrix(cluster(self.clusters[i:i+10]), cluster(self.clusters[0:10]))])
            self.assertEqual(d, cluster.complete_linkage(cluster(self.clusters[i:i+10]), cluster(self.clusters[0:10])))
    def test_normalize(self):
        for i in range(0,len(self.clusters),10):
            for i in cluster(self.clusters[i:i+10]).normalized():
                self.assertTrue(point([0]*3) <= i <= point([1]*3))

class cluster_set(object):
    ''' models self as a set of clusters'''

    def __init__(self, data:list[cluster]):
        self.clusters = data
    def __getitem__(self, index):
        return self.clusters[index]
    def __setitem__(self, index, item):
        self.clusters[index] = item
    def __repr__(self):
        return str(self.clusters)
        
    def is_close(self, other, min_diff = 0.01, f = point.euclidean_distance):
        if other == []:
            return False
        if len(other.clusters) != len(self.clusters):
            return True
        return max([f(a.centroid(),b.centroid()) for a,b in zip(self.clusters, other.clusters)]) < min_diff
    def copy(self):
        return cluster_set(self.clusters.copy())
    
    def plot(self: "cluster_set", file_name: str, labels: list[str], attributes: list = [0,1]) -> "plt.figure":
        plt.figure()
        plt.title(labels[0])
        plt.xlabel(labels[1])
        plt.ylabel(labels[2])
        L = ["red", "green", "blue"]
        count = 0
        for cluster in self.clusters:
            cluster.plot(L[count%3], attributes)
            count += 1
        plt.savefig(file_name)
        plt.close()
    
    def append(self, cluster):
        self.clusters.append(cluster)
        
class test_cluster_set(unittest.TestCase):
    def setUp(self):
        self.clusters = [cluster([point([random.random() for _ in range(3)]) for _ in range(10)]) for _ in range(10)]

    
if __name__ == '__main__':
    unittest.main()
