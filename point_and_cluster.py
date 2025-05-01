import pandas as pd
import numpy as np
class point (object):
    """assumes self is a n-dimensional position vector for a point, models self as a array of attributes"""

    def __init__(self, attributes):
        self.attributes = np.array(attributes)
    def __repr__(self):
        return str(self.attributes)
    def __eq__(self, other):
        if len(self.attributes) != len(other.attributes):
            return False 
        ans = True
        for i in (abs(self.attributes - other.attributes) < 0.0001):
            ans &= i
        return ans
    def __len__(self):
        return len(self.attributes)
    def __hash__(self):
        return hash(tuple(np.round(self.attributes, decimals=3)))
    
    #amazingly this works cause np.array(point) works and np.array(a number) = that number
    def __add__(self, other):
        return (point(self.attributes + np.array(other)))
    def __sub__(self, other):
        return self + other * -1
    def __mul__(self, other):
        return (point(self.attributes * np.array(other)))
    def __truediv__(self, other):  
        return (point(self.attributes / np.array(other)))
    def __pow__(self, other):
        return (point(self.attributes ** np.array(other)))
    
    def __getitem__(self, index):
        return self.attributes[index]
    def __setitem__(self, index, value):
        self.attributes[index] = value
    def __iter__(self): 
        return iter(self.attributes)
    def __contains__(self, item): 
        return item in self.attributes
    
    def __ge__(self,other):
        return list(self.attributes) >= list(other.attributes)
    def __gt__(self,other):
        return list(self.attributes) > list(other.attributes)
    def __lt__(self,other):
        return list(self.attributes) < list(other.attributes)
    def __le__(self,other):
        return list(self.attributes) <= list(other.attributes)
    def __abs__(self):
        return point(abs(self.attributes))
    
    def length(self):
        return self.euclidean_distance(point([0]*len(self.attributes)))
    def manhattan_distance(self, other):
        return sum(abs(self.attributes - other.attributes))
    def euclidean_distance(self, other):
        return sum((self.attributes - other.attributes)**2)**0.5
    def dot(self, other):
        return sum(self.attributes * other.attributes)
    def copy(self):
        return point(self.attributes)
    
    def get_attributes(self):
        return list(self.attributes)
    def set_attributes(self, attributes):
        self.attributes = np.array(attributes)

import unittest     
import random  
class test_point(unittest.TestCase):

    def setUp(self):
        self.trials = 100
        self.dimensions = 3
        self.points = [[ random.random() for _ in range(self.dimensions)] for __ in range(self.trials)]
    
    def test_string(self):
        for i in self.points:
            self.assertEqual(str(np.array(i)), str(point(i)))
    def test_eq(self):
        for i in self.points:
            self.assertEqual(point(i), point(i))
            self.assertNotEqual(point(i), point(i + [0]))
            self.assertNotEqual(point(i), point([j + 0.01 for j in i]))
            p = point(i)
            p[0] += 0.1
            self.assertNotEqual(p,point(i))
    def test_hash(self):
        for i in self.points:
            self.assertTrue(isinstance(hash(point(i)),int))
            self.assertNotEqual(hash(point(i)), hash(point([j + 0.01 for j in i])))
    def test_op_num(self):
        r = random.random() + 0.01
        for i in self.points:
            self.assertEqual(((point(i) +r) - r), point(i))
            self.assertEqual(((point(i)*r)/r),point(i))
            self.assertEqual(((point(i)**r)**(1/r)), point(i))
    def test_len(self):
        for i in self.points:
            self.assertEqual(len(i),len(point(i)))
    def test_item_access(self):
        for i in self.points:
            p = point(i)
            p[0] = p[0] + 1
            self.assertNotEqual(i[0],p[0])
    def test_iter_contain(self):
        ans =True
        for i in self.points:
            for j in point(i):
                ans &= j in point(i)
        self.assertTrue(ans)
    def test_euclidean_dist(self):
        for i in range(1,len(self.points)):
            d1 = point(self.points[i-1]).euclidean_distance(point(self.points[i]))
            d2 = (sum((np.array(self.points[i-1]) - np.array(self.points[i]))**2))**0.5
            self. assertAlmostEqual(d1,d2)
    def test_manhattan_dist(self):
        for i in range(1,len(self.points)):
            d1 = point(self.points[i-1]).manhattan_distance(point(self.points[i]))
            d2 = sum(abs(np.array(self.points[i-1]) - np.array(self.points[i])))
            self. assertAlmostEqual(d1,d2)
    def test_dot(self):
        for i in range(1,len(self.points)):
            a = point(self.points[i-1]).dot(point(self.points[i]))
            b = sum(np.array(self.points[i-1])*np.array(self.points[i]))
            self.assertEqual(a,b)
    def test_copy(self):
        for i in self.points:
            a = point(i)
            b = a
            c = a.copy()
            a[0] += 1
            self.assertEqual(a,b)
            self.assertNotEqual(a,c)
    def test_get_set(self):
        for i in self.points:
            p = point(i)
            p.set_attributes(i)
            self.assertEqual(point(i).get_attributes(), i)

class cluster(object):
    '''assumes self is a cluster of points, models self as a list of point objects'''

    def __init__(self,data:list[point]):
        if isinstance(data, pd.DataFrame):
            self.points = list(point(x) for x in data.values.tolist())
        else: 
            self.points = data
    def __eq__(self,other):
        return sorted(self.points) == sorted(other.points) 
    def __repr__(self):
        return str(self.points)
    def __len__(self):
        return len(self.points)
    def __hash__(self):
        return hash(tuple(self.points))

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
    def normalized(self):
        min = self.points[0].copy()
        max = self.points[0].copy()
        for i in self.points:
            for j in range(len(self.points[0])):
                if i[j] < min[j]:
                    min[j] = i[j]
                if i[j] > max[j]:
                    max[j] = i[j]

        if min == max: 
            return cluster([point([1]*len(min)) for _ in self.points])
        else:
            return cluster([(p - min)/(max-min) for p in self.points])
    def merged(self, other):
        return cluster(self.points + other.points)
    def copy(self):
        return cluster([p.copy() for p in self.points])
    
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
            self.assertEqual(op(c,r), op(c,r) + 0.000001)
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

if __name__ == '__main__':
    unittest.main()
