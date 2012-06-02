# Decision Tree

# Katherine Siegal & Veronica Lynn

# May 15, 2012

import sys
from math import log
from random import randint

def decisiondattree(categories, data, node, level):
    """Prints out a decision tree"""

    # Base case: make final split, then give final decision
    if len(categories) == 2:
        tree[level].append((node, categories[0]))
        print "--"*(len(tree)-level) + "if", node + ", split on", categories[0]
        
        
        for child in getChildren(data, 0):           
            childData = [x for x in data if x[0] == child]
            yesNo = getYesNo(childData)
            if yesNo[0] > yesNo[1]:
                tree[level-1].append((node, "YES"))
                print "--"*(len(tree)-level + 1) + "if", child + ", then YES"
            elif yesNo[0] < yesNo[1]:
                tree[level-1].append((node, "NO"))
                print "--"*(len(tree)-level + 1) + "if", child + ", then NO"
            else:
                parentYesNo = getYesNo(data)
                if parentYesNo[0] >= parentYesNo[1]:
                    tree[level-1].append((node, "YES"))
                    print "--"*(len(tree)-level + 1) + "if", child + ", then YES"
                else:
                    tree[level-1].append((node, "NO"))
                    print "--"*(len(tree)-level + 1) + "if", child + ", then NO"
        return
    
    maxIG = float('-infinity')
    maxCategory = None
    
    entropyOrig = getEntropy(data)
    
    # If a node is certain (100% yes or no), then don't split on it
    if entropyOrig == 0:
        yesNo = getYesNo(data)
        if yesNo[0] == 0:
            tree[level].append((node, "NO"))
            print "--"*(len(tree)-level) + "if", node + ", then NO"
        else:
            tree[level].append((node, "YES"))
            print "--"*(len(tree)-level) + "if", node + ", then YES"
        return
    else:
        for category in categories[:-1]:
            # For every possible split, calculate information gains
            entropyWeightedAvg = 0
            index = categories.index(category)
            for child in getChildren(data, index):           
                childData = [x for x in data if x[index] == child]
                entropyWeightedAvg += getEntropy(childData) * len(childData) / len(data)
            
            infoGain = entropyOrig - entropyWeightedAvg
            
            # Check if this is the best split yet (minimizes information gain)
            if infoGain > maxIG:
                maxIG = infoGain
                maxCategory = category
                
    # Make the best split
    i = categories.index(maxCategory)
    newCategories = categories[:i] + categories[i+1:]
    
    
    tree[level].append((node, maxCategory))
    print "--"*(len(tree)-level) + "if", node + ", split on", maxCategory
    
    # Recursively split tree at next level
    for child in getChildren(data,i):
        childData = [x for x in data if x[i] == child]
        newData = [x[:i] + x[i+1:] for x in childData]
        decisiondattree(newCategories, newData, child, level-1)
    
    
    
def getEntropy(data):
    yesNo = getYesNo(data)
    
    # To avoid gross
    if yesNo[0] == 0 or yesNo[1] == 0:
        return 0
    
    p_y = float(yesNo[0]) / len(data)
    p_n = float(yesNo[1]) / len(data)
    entropy = p_y * -log(p_y, 2) + p_n * -log(p_n, 2)
    
    return entropy

def getChildren(data, index):
    children = []
    for entry in data:
        if entry[index] not in children:
            children.append(entry[index])
    
    return children

def getYesNo(data):
    """Returns as a tuple the number of yes and no outcomes in a given data set: (# of yes, # of no)"""
    
    yes = 0
    for entry in data:
        if entry[-1] == "yes":
            yes += 1
    return (yes, len(data)-yes)

if __name__ == "__main__":
    path = sys.argv[1]
    f = open(path, 'r')
    
    categories = f.readline().strip().split("\t")
        
    data = []
    for line in f:
        data.append(line.strip().split("\t"))

    f.close()

    tree = []
    for i in range(len(categories)):
        tree.append([])

    splits = decisiondattree(categories, data, "root", len(categories)-1)
