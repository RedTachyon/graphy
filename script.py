import os
from multiprocessing import Pool
import matplotlib.pyplot as plt
import numpy as np
from graph import Graph
from gui import GrApp, show
from tqdm import tqdm
import pickle

def run_experiment(N, K, prob):
    graph = Graph(N, K)
    graph.WS_model(prob)
    
    degrees = []
    for node in graph.nodes:
        degrees.append(graph.degree(node))
    degrees = np.array(degrees)
    
    unique, counts = np.unique(degrees, return_counts=True)
    for i in range(np.max(unique)):
        if i not in unique:
            unique = np.insert(unique, i, i)
            counts = np.insert(counts, i, 0)
    counts = counts[unique.argsort()]
    unique.sort()
    
    return counts / np.sum(counts)

def vstack(arr1, arr2):
    '''Assumes that arr2 is 1D; Stacks two array vertically, filling with zeros if needed'''
    #assert len(arr2.shape) == 1
    
    if arr1.shape[-1] == arr2.shape[-1]:
        return np.vstack((arr1, arr2))
    elif arr1.shape[-1] < arr2.shape[-1]:
        if len(arr1.shape) > 1:
            zeros = np.zeros((arr2.shape[-1] - arr1.shape[-1], arr1.shape[0]))
        else:
            zeros = np.zeros((arr2.shape[-1] - arr1.shape[-1],))
        tarr1 = np.hstack((arr1, zeros.T))
        return np.vstack((tarr1, arr2))
    
    elif arr1.shape[-1] > arr2.shape[-1]:
        zeros = np.zeros((arr1.shape[-1] - arr2.shape[-1],))
        tarr2 = np.hstack((arr2, zeros.T))
        return np.vstack((arr1, tarr2))

def rep_experiment(reps, N=10, K=2, prob=0.5):
    results = run_experiment(N, K, prob)
    for _ in tqdm(range(reps - 1)):
        results = vstack(results, run_experiment(N, K, prob))
        
    return results



data_dict = {}

def process_prob(prob):
    prob = prob/10
    data_dict[prob] = rep_experiment(1000, N=1000, prob=prob)

if __name__ == '__main__':
    pool = Pool(5)
    pool.map(process_prob, range(1,11))
    with open('data.pickle', 'wb') as f:
        pickle.dump(data_dict, f)