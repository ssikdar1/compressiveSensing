
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
import difflib
import matplotlib.pyplot as plt
import cPickle as pickle
import networkx as nx


# In[3]:

nodes = pd.read_excel('nodes.xlsx')
edges = pd.read_excel('edges.xlsx')


# In[15]:

nodes.to_pickle('nodes.pkl')
edges.to_pickle('edges.pkl')


# In[6]:

nodes = pd.read_pickle('nodes.pkl')
edges = pd.read_pickle('edges.pkl')


# In[18]:

nodes[nodes['GUID']=='SEED-1']


# In[19]:

nodes[nodes['GUID']=='SEED-2']


# In[27]:

len(edges[edges['GUID_1']=='SEED-1'])


# In[32]:

len(edges[edges['GUID_2']=='SEED-2'])


# In[7]:

edges_new = edges.groupby('GUID_1')


# In[333]:

guid_1 = edges['GUID_1'].tolist()
guid_2 = edges['GUID_2'].tolist()
distance = edges['TCS'].tolist()

guid_1 = [str(key) for key in guid_1]
guid_2 = [str(key) for key in guid_2]
distance = [(1 - float(key)) for key in tcs]


# In[335]:

adj_list=[]
for i in range(0,len(guid_1)):
    adj_list.append(guid_1[i] + ' ' + guid_2[i] + ' ' + str(distance[i]))


# In[361]:

G = nx.parse_edgelist(adj_list, nodetype = str, data=(('weight',float),))


# In[362]:

paths = nx.shortest_path(G,'SEED-1','SEED-2',weight='weight')


# In[363]:

path_distance = 0
for i in range(0,len(paths)-2):
    node1 = paths[i]
    node2 = paths[i+1]
    path_distance += G[node1][node2]['weight']
print "Final path distance"    
print path_distance


# In[364]:

for path in paths:
    print (path)


# In[344]:

for node in paths:
    print nodes[nodes['GUID']== node]
    print "---------------------------"


# In[365]:

G.remove_edge(paths[-1],paths[-2])


# In[366]:

paths = nx.shortest_path(G,'SEED-1','SEED-2',weight='weight')


# In[367]:

path_distance = 0
for i in range(0,len(paths)-2):
    node1 = paths[i]
    node2 = paths[i+1]
    path_distance += G[node1][node2]['weight']
print "Final path distance"    
print path_distance


# In[348]:

for node in paths:
    print node


# In[368]:

for node in paths:
    print nodes[nodes['GUID']== node]
    print "---------------------------"


# In[369]:

G.remove_edge(paths[-1],paths[-2])


# In[370]:

paths = nx.shortest_path(G,'SEED-1','SEED-2',weight='weight')


# In[ ]:



