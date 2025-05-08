# OOP approach
from cluster import *
import pandas as pd
import random

def KMeans(k: int,data,cutoff = cluster_set.is_close, max_iterations = 100):
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
means , clusters, __ = KMeans(2,data)
clusters.append(means)
clusters.plot("Dew4", ["visibility", "Dew_Point (°C)", "Visibility (km)"],[0,4])
clusters.plot("Dew3", ["temprature", "Dew_Point (°C)", "Temperature (°C)"],[0,3])
clusters.plot("Dew2", ["Preassure", "Dew_Point (°C)", "Pressure (hPa)"],[0,2])
clusters.plot("Dew1", ["Humidity", "Dew_Point (°C)", "Humidity (%)"],[0,1])