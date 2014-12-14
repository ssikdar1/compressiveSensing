
# coding: utf-8

# In[29]:

import pandas as pd
import numpy as np
import difflib
import matplotlib.pyplot as plt
import cPickle as pickle
import networkx as nx
import random


# In[43]:

#parameters
numMeasurements = 100
treeDepth = 2


# In[44]:

#load the node and edge data
nodes = pd.read_pickle('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\nodes.pkl')
edges = pd.read_pickle('C:\Users\Shan\Documents\GitHub\\compressiveSensing\edges.pkl')


# In[45]:

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


# In[46]:

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
        



# In[47]:


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



# In[70]:

#
# Now need to obtain the measurements y_i for each randomly chosen node
#

y = [] #this is our y in y = Ax, each entry y_i a measurement sum
s = (len(randomNodes),len(nodes))
A = np.zeros(s)

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
#             measurement_sum = 0
            pass
    y.append(measurement_sum)
    
    #for every node in the clique change its corresponding position to 1
    for gid in nodesInClique:
        j = int(nodes[nodes['GUID'] == gid].index.values.tolist()[0])
        A[i,j] = 1
    


# In[49]:

print nodesInClique 
print y


# In[71]:

print A


# In[72]:

# just checking there are actually 1's in this A matrix 
for k in A:
    indices = [i for i, x in enumerate(k) if x == 1]
    print indices


# In[73]:

#write the y and A to spereate files
import csv
with open('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\y_vector.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerow(y)


# In[80]:

with open('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\A_matrix.csv', 'wb') as f1:
    writer1 = csv.writer(f1)
    for row in A:
        writer1.writerow(row)


# In[75]:

# np.savetxt('C:\Users\Shan\Documents\GitHub\\compressiveSensing\\A_matrix.csv', A, delimiter=',')


                
                
# In[78]:

A.shape


# In[ ]:



