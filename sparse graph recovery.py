
# coding: utf-8

# In[88]:

import pandas as pd
import numpy as np
import difflib
import matplotlib.pyplot as plt
import cPickle as pickle
import networkx as nx
import random


# In[89]:

#parameters
numMeasurements = 10
treeDepth = 2


# In[90]:

#load the node and edge data
nodes = pd.read_pickle('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\nodes.pkl')
edges = pd.read_pickle('C:\Users\Shan\Documents\GitHub\\compressiveSensing\edges.pkl')


# In[91]:

#
# create graph
#
guid_1 = edges['GUID_1'].tolist()
guid_2 = edges['GUID_2'].tolist()
distance = edges['TCS'].tolist()

guid_1 = [str(key) for key in guid_1]
guid_2 = [str(key) for key in guid_2]
distance = [(1 - float(key)) for key in distance]

adj_list=[]
for i in range(0,len(guid_1)):
    adj_list.append(guid_1[i] + ' ' + guid_2[i] + ' ' + str(distance[i]))
G = nx.parse_edgelist(adj_list, nodetype = str, data=(('weight',float),))


# In[92]:

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
    if (len(edges[(edges['GUID_1'] == guid) | (edges['GUID_2'] == guid)]) != 0):
        #append number if so
         randomNodes.append(nodeNum)
            
print randomNodes

#check and make sure all random nodes are in the connected component
for i in range(0,len(randomNodes)): 
    guid = nodes.loc[randomNodes[i]]['GUID']
    tmp =  len(edges[(edges['GUID_1'] == guid) | (edges['GUID_2'] == guid)])
    if(tmp == 0):
        print str(randomNodes[i]) + '\tNot in Conncected component'
        



# In[117]:



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



# In[ ]:

#
# Now need to obtain the measurements y_i for each randomly chosen node
#

y = [] #this is our y in y = Ax, each entry y_i a measurement sum
A = []

#iterate through all our random chosen nodes
for i in range(0,len(randomNodes)): 
    #for each node get all the vertices that make the clique up to the depth 
    
    nodesInClique = []
    #get all nodes up to the tree depth
    for d in range(0,treeDepth):
        drillToDepth(nodes.loc[randomNodes[i]]['GUID'], 0, d, nodesInClique)

    #now for each node in this clique find the shortest path
    #get it's length and add it to a rolling sum

    measurement_sum = 0
    for n in nodesInClique:
        try:
            measurement_sum += len(nx.shortest_path(G,'SEED-1',n,weight='weight'))
        except:
            #no networkx path to seed-1
            measurement_sum = 0
    y.append(measurement_sum)
    
    irow =[]
    row_iterator = nodes.iterrows()
    for i, row in row_iterator:
        if row['GUID'] in nodesInClique:
            irow.append(1)
        else:
            irow.append(0)
    A.append(irow)


# In[138]:

print nodesInClique 
print y


# In[112]:




# In[114]:

#now for each node look at tree of depth h

    guid = nodes.loc[randomNodes[i]]['GUID']
    #  G[1]  adjacency dict keyed by neighbor to edge attributes Note: you should not change this dict manually!
    print len(G[guid])


# In[108]:

for key in G['ID-a57dd69b-916c-4a39-8d95-bd9b76c64f38']:
    print key


# In[85]:

H = nx.Graph()
H.add_node(1)


# In[87]:

len(H[1])


                
                
# In[ ]:



