#Gilbert Velasquez
# CS2302 MW 1:30-2:50
# lab 6
# Instructor Olac Fuentes
# TA Anindita Nath and Maliheh Zargaran
# Date of Last Modification 4/14/2019

#The purpose of this lab was to get a better understanding of Disjoint Set Forests. In this lab we were to use the DSF to create a maze that had exactly 
#one path. This was achieved by using DSF and the idea that we can get a single path if we have a DSF with only one root. This lab taught me a lot! Espically not to overthink things!



import matplotlib.pyplot as plt
import numpy as np
import random
import time

def DisjointSetForest(size):
    return np.zeros(size,dtype=np.int)-1
        
def dsfToSetList(S):
    #Returns aa list containing the sets encoded in S
    sets = [ [] for i in range(len(S)) ]
    for i in range(len(S)):
        sets[find(S,i)].append(i)
    sets = [x for x in sets if x != []]
    return sets

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
         
def union_by_size(S,i,j):
    # if i is a root, S[i] = -number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]: # j's tree is larger
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri
            
def NumSets(S): # Returns the number of sets in a DSF
    count = 0
    for i in range(len(S)):
        if S[i]< 0:
            count += 1
    return count 
        
    
def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

plt.close("all") 
maze_rows = 10
maze_cols = 15

walls = wall_list(maze_rows,maze_cols)
DSF = DisjointSetForest(maze_rows*maze_cols) # Creates DSF

walls2 = wall_list(maze_rows,maze_cols) # second wall list for use with compressions 
DSF2 = DisjointSetForest(maze_rows*maze_cols)# Second DSF for compressions 
    

draw_maze(walls,maze_rows,maze_cols,cell_nums=True) 

start = time.time() #Time for uninons without compressions 
while NumSets(DSF)>1: #Check to see if we have more than one set 
    d = random.randint(0,len(walls)-1) #select a random wall
    if find(DSF,walls[d][0]) != find(DSF,walls[d][1]): # if they belong to different sets 
        #print(find(DSF,walls[d][0]))
        #print(find(DSF,walls[d][1]))
        union(DSF,walls[d][0],walls[d][1]) #here we combine them without compressions
           #print(S)
           #print('removing wall ',walls[d])
        walls.pop(d) # get rid of that wall from our list 
end = time.time()
print("Time for Regular Union" , end - start)

start2 = time.time() # Time for size and compressions union
while NumSets(DSF2)>1: #Check to see if we have more than one set 
    d = random.randint(0,len(walls2)-1)
    if find(DSF2,walls2[d][0]) != find(DSF2,walls2[d][1]): # if they belong to different sets 
        union_by_size(DSF2,walls2[d][0],walls2[d][1]) #here we combine them here with size and compression union
        walls2.pop(d) # get rid of that wall from our list 
end2 = time.time()

print("Time for Union by Size with Compression", end2 - start2)
draw_maze(walls,maze_rows,maze_cols)   #Draws maze without compressions             
draw_maze(walls2,maze_rows,maze_cols) #Draws maze with size and compression uninon