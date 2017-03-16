#!/usr/bin/env python3
''' Grow a randomized district plan starting from a graph of parts.
'''
import sys, networkx, random, numpy, itertools, functools, operator, time

_, district_str, graph_path = sys.argv
district_count = int(district_str)

setup_time = time.time()

districts = range(1, 1+district_count)
graph = networkx.readwrite.read_edgelist(graph_path, nodetype=int)
node_count = len(graph.nodes())

print('{} nodes into {} districts'.format(node_count, district_count), file=sys.stderr)

iterations = numpy.zeros((node_count * 2, node_count), int)
node_indexes = numpy.array(range(node_count))

start_time = time.time()

start = list(graph.nodes())
random.shuffle(start)

for (district, node) in zip(districts, start):
    iterations[0,node] = district

for (generation, district) in enumerate(itertools.cycle(districts)):
    free_nodes = node_indexes[iterations[generation,:] == 0]
    
    # if no free space remains, clip the array and get out
    if len(free_nodes) == 0:
        iterations = iterations[:generation+1,:]
        break
    
    # list of node IDs owned by the current district
    district_nodes = node_indexes[iterations[generation,:] == district]

    # list of lists of node IDs neighboring the current district
    neighbor_lists = [graph.neighbors(n) for n in district_nodes]

    # list of free nodes available to the current district
    neighbors = functools.reduce(operator.add, neighbor_lists)
    neighbors = list(set(neighbors) & set(free_nodes))

    # copy the current generation forward
    iterations[generation+1,:] = iterations[generation,:]

    # pick a random available neighbor to fill
    if neighbors:
        iterations[generation+1,random.choice(neighbors)] = district
    
    if generation == iterations.shape[0] - 2:
        print('oh no', file=sys.stderr)
        exit(1)

end_time = time.time()

print('done in {:.3f} seconds with {:.3f} setup'.format(end_time - start_time, start_time - setup_time), file=sys.stderr)
print(' '.join(map(str, iterations[-1,:])), file=sys.stdout)
