
# coding: utf-8

# In[13]:

import pandas as pd
import numpy as np
import difflib
import matplotlib.pyplot as plt
import cPickle as pickle
import networkx as nx
import random


# In[14]:

#parameters
numMeasurements = 100
treeDepth = 3


# In[15]:

#load the node and edge data
original_nodes = pd.read_pickle('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\nodes.pkl')
edges = pd.read_pickle('C:\Users\Shan\Documents\GitHub\\compressiveSensing\edges.pkl')


# In[16]:

#
# create the dataframes for a smaller node set to get a smaller A matrix
#

#get only the nodes that are in the edge set
new = pd.merge(original_nodes,edges, left_on='GUID', right_on = 'GUID_1', how='right')
new2 = pd.merge(original_nodes,edges, left_on='GUID', right_on = 'GUID_2', how='right')
small_set = pd.merge(new,new2, on='GUID', how='outer')
reducedNodes = pd.DataFrame({'count' : small_set.groupby( ["GUID"] ).size()}).reset_index()

#get rid of all nodes of degree 1
reducedNodes2 = reducedNodes[reducedNodes['count'] > 1]
print len(reducedNodes)

nodes = reducedNodes2.reset_index()
nodes_list = nodes['GUID'].tolist()
# reducedNodes['GUID']
# reducedNodes[reducedNodes['GUID'].str.contains('SEED')]
# reducedNodes.sort(columns='count',ascending=False)


# In[17]:

edges_pruned = edges[edges['GUID_1'].isin(nodes['GUID'])]
edges_pruned = edges_pruned[edges_pruned['GUID_2'].isin(nodes['GUID'])]
print len(edges_pruned)
print len(edges)
edges_pruned


# In[18]:

#
# create graph
#

guid_1 = edges_pruned['GUID_1'].tolist()
guid_2 = edges_pruned['GUID_2'].tolist()


distance = edges_pruned['TCS'].tolist()

guid_1 = [str(key) for key in guid_1]
guid_2 = [str(key) for key in guid_2]
distance = [(1 - float(key)) for key in distance]

adj_list=[]
for i in range(0,len(guid_1)):
    adj_list.append(guid_1[i] + ' ' + guid_2[i] + ' ' + str(distance[i]))
G = nx.parse_edgelist(adj_list, nodetype = str, data=(('weight',float),))


# In[19]:

#get the m << n measurements, choose m random vertices and put them into a list to iterate through later
randomNodes = []

# for i in range(0, numMeasurements):
#     randomNodes.append(random.randint(1, len(nodes)))
#     #I Have to check if they are in the connected component don't I???

#
# get random vertices from connected components
#
while(len(randomNodes) != numMeasurements):
    #get random int
    nodeNum = random.randint(1, len(nodes))
    
    #check to see if its in the connected component by checking to see if the vertex is in the edge set
    guid = nodes.loc[nodeNum]['GUID']
    if (len(edges_pruned[(edges_pruned['GUID_1'] == guid) | (edges_pruned['GUID_2'] == guid)]) != 0) and (len(nodes[nodes['GUID'] == guid]) != 0) :
        #append number if so
         randomNodes.append(nodeNum)
            
print randomNodes

#check and make sure all random nodes are in the connected component
for i in range(0,len(randomNodes)): 
    guid = nodes.loc[randomNodes[i]]['GUID']
    tmp =  len(edges_pruned[(edges_pruned['GUID_1'] == guid) | (edges_pruned['GUID_2'] == guid)])
    if(tmp == 0):
        print str(randomNodes[i]) + '\tNot in Conncected component'
        



# In[20]:




# In[20]:


#
# Use this function to get all nodes at a certain depth
# Current level is initially 0 and starts at the randomly chosen vertex
# the recursively go down if the current level is the depth append the node guid and return
# else go through all the nodes possible neighbors and increment current level
#
def drillToDepth(node_guid, curr_level, depth, result):
    if(curr_level == depth):
        result.append(node_guid)
    else:
        for key in G[node_guid]:
            drillToDepth (key, curr_level + 1, depth, result);



# In[21]:

def pathDistance(path):
    path_distance = 0
    for i in range(0,len(path)-2):
        node1 = path[i]
        node2 = path[i+1]
        path_distance += G[node1][node2]['weight']
    return path_distance


# In[ ]:

#
# Now need to obtain the measurements y_i for each randomly chosen node
#

y = [] #this is our y in y = Ax, each entry y_i a measurement sum
s = (len(randomNodes),len(nodes))
A = np.zeros(s)

cliqueSizes = []

#shortest path between Seed-1 and Seed 2
seed_path = nx.shortest_path(G,'SEED-1','SEED-2',weight='weight')
seed_nodes = [node for node in seed_path]

#iterate through all our random chosen nodes
for i in range(0,len(randomNodes)): 
    #for each node get all the vertices that make the clique up to the depth 
    
    nodesInClique = []
    #get all nodes up to the tree depth
    for d in range(0,treeDepth):
        drillToDepth(nodes.loc[randomNodes[i]]['GUID'], 0, d, nodesInClique)

    cliqueSizes.append(len(nodesInClique))
    
    #now for each node in this clique find the shortest path
    #go throught the click and take the smallest shortest path

    measurement_sum = 0
    
    for n in nodesInClique:
        try:
            shortest_dist = 1000000
            for node in seed_nodes:
                path = nx.shortest_path(G,n,node,weight='weight')
                path_dist = pathDistance(path)
                if path_dist < shortest_dist:
                    shortest_dist = path_dist

            measurement_sum += shortest_dist
        except:
            #no networkx path to seed-1
            measurement_sum = 0
#             print "shortest path not found"
            pass
    y.append(measurement_sum)
    
    #for every node in the clique change its corresponding position to 1
    for gid in nodesInClique:
        
        j = int(nodes[nodes['GUID'] == gid].index.values.tolist()[0])
        A[i,j] = 1
        


# In[10]:




# In[10]:




# In[11]:

print cliqueSizes 
print y


# In[12]:

print A


# In[13]:

# just checking there are actually 1's in this A matrix 
for k in A:
    indices = [i for i, x in enumerate(k) if x == 1]
    print indices


# In[22]:

A[A == 0] = 1000
print A


# In[23]:

#write the y and A to spereate files
import csv
with open('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\y_vector.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(y)


# In[25]:

import scipy.io as sio
sio.savemat('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\sensingMatrix.mat', {'A':A})


                
                
# In[17]:

from sklearn.linear_model import Lasso, Ridge
rgr_lasso = Lasso(alpha = 0.001)
rgr_lasso.fit(A,y)


# In[18]:

rec_l1 = rgr_lasso.coef_
print rec_l1


# In[20]:

indices = [i for i, x in enumerate(rec_l1) if x == 0]
# print indices


# In[21]:

import csv
with open('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\ans_vector.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(rec_l1)


# In[33]:




# In[31]:




# In[219]:

print len(edges)
print len(new)
print len(new2)
print len(small_set)


# In[175]:

tmp1 = nodes[nodes['GUID'].isin(edges['GUID_1']) & ~(nodes['GUID'].isin(edges['GUID_2']))]
tmp2 = nodes[nodes['GUID'].isin(edges['GUID_2']) & ~(nodes['GUID'].isin(edges['GUID_1']))].drop_duplicates()
tmp3 = pd.concat([tmp1, tmp2]).drop_duplicates()


# In[177]:

len(tmp3)


# In[ ]:

import scipy.io
mat = scipy.io.loadmat('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\sensingMatrix.mat')


# In[1]:

from numpy import genfromtxt
X = genfromtxt('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\regressionX.csv',delimiter=',')


# In[2]:

X


# In[8]:

indices = []
for index in range(0,len(X)):
    if X[index] != 0:
        indices.append(index)


# In[22]:

len(nodes)


# In[35]:

df = pd.DataFrame()
for element in indices:
#     print nodes_list[element]
   df = df.append(original_nodes[original_nodes['GUID'] == nodes.loc[element]['GUID']])
#     f.write(str(original_nodes[original_nodes['GUID'] == nodes.loc[element]['GUID']]))
#     f.write('\n')


# In[43]:

df.to_csv(sep=',',encoding='utf-8')


# In[ ]:



