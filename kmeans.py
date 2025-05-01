#functional approach
#this is one of my earlier works, back when i firsst started to code
import pandas as pd
#to normalize my data
def normalize(column):
    min_val = column.min()
    max_val = column.max()
    return (column - min_val) / (max_val - min_val)
#to generate distance matrix
def DistanceMatrix(k, mean_dictionary = {}):
    md = mean_dictionary
    distance_matrix_list = []
    dl = distance_matrix_list
    if not md:
        for i in range(k):
            md[i] = [dp[i],h[i],p[i],t[i],v[i]]
    for i in range(len(md)):
        temp = []
        for j in range(len(table)):
            temp += [((dp[j]-md[i][0])**2+(h[j]-md[i][1])**2+(p[j]-md[i][2])**2+(t[j]-md[i][3])**2+(v[j]-md[i][4])**2)**0.5]
        dl += [temp]
    return dl
#to generate assignment list
def assignment(k, distance_matrix_list):
    dl = distance_matrix_list
    assignment_list = []
    al = assignment_list
    for i in range(len(dl[0])):
        temp = []
        for j in range(k):
            temp += [dl[j][i]]
        min_val = temp[0]
        for x in range(len(temp)):
            if temp[x] <= min_val:
                min_val = temp[x]
                group = x
        al += [group]
    return al
#recomputation of means
def mean(k,assignment_list):
    cluster_count_list = []
    cl = cluster_count_list
    al = assignment_list
    for i in range(k):
        cl += [al.count(i)]
    mean_dictionary = {}
    md = mean_dictionary
    for i in range(k):
        md[i] =[0,0,0,0,0]
    for i in range(len(al)):
        md[al[i]][0] += dp[i]/(cl[al[i]])
        md[al[i]][1] += h[i]/(cl[al[i]])
        md[al[i]][2] += p[i]/(cl[al[i]])
        md[al[i]][3] += t[i]/(cl[al[i]])
        md[al[i]][4] += v[i]/(cl[al[i]])
    return md
#generating final means
def kmeans(k,n):
    md = {0: [11,43,1016,21,1], 1:[15,100,1017,15,1]}
    for i in range(n):
        dl = DistanceMatrix(k, md)
        al = assignment(k, dl)
        md = mean(k,al)
    return md
#main
table = pd.read_csv("final_weather_data.csv")
dp = table["Dew_Point (°C)"]
h = table["Humidity (%)"]
p = table["Pressure (hPa)"]
t = table["Temperature (°C)"]
v = table["Visibility (km)"]
dp = normalize(dp)
h = normalize(h)
p = normalize(p)
t = normalize(t)
v = normalize(v) 
#print("means:",kmeans(2,1))
#dl = DistanceMatrix(2)
#al = assignment(2,dl)
#print("grouping of 04-jan-2015: cluster",al[2]+1)
#print("distance of 12-jan-2016 from 01-jan-2015:",dl[0][323])