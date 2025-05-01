# OOP approach
from point_and_cluster import *
import pandas as pd
import random

def KMeans(k,data,cutoff = cluster_set.is_close, max_iterations = 100):
    ''' assumes data is a cluster and k is a possitive integer
        returns the k clusters that most closely approximate ndimensional spheres 
        uses kmeans method'''
    
    assert k < len(data)

    #initialization
    means = cluster(random.sample(data.get_points(), k)) # intial mean selection
    distance_matrix = data.distance_matrix(means) 
    clusters = []
    old_clusters = []
    iterations = 0
    
    while iterations < max_iterations:

        old_clusters = clusters.copy()
        clusters = cluster_set([cluster([]) for i in range(k)])

        #cluster assignment
        for i in range(len(data)):
            min_dist = distance_matrix[i][0]
            cluster_assignment = 0
            for j in range(1, k):
                if distance_matrix[i][j] < min_dist:
                    min_dist = distance_matrix[i][j]
                    cluster_assignment = j
            clusters[cluster_assignment].append(data[i])

        #re-calculation of means and distance_matrix
        means = cluster([c.centroid() for c in clusters])
        distance_matrix = data.distance_matrix(means)

        iterations += 1
        
        if cutoff(clusters, old_clusters):
            break
        
    return means,clusters,distance_matrix

#example
table = pd.read_csv("final_weather_data.csv")
data = table[["Dew_Point (°C)", "Humidity (%)", "Pressure (hPa)", "Temperature (°C)", "Visibility (km)"]]
data = cluster(data).normalized()
print(KMeans(10,data))