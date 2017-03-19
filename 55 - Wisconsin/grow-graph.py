#!/usr/bin/env python3
''' Grow a randomized district plan starting from a graph of parts.
'''
import sys, networkx, random, numpy, itertools, functools, operator, time, math, hashlib, os
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('district_count', type=int, help='Number of districts')
parser.add_argument('graph_path', type=str, help='Path to graph file')

parser.add_argument('--iterations', '-n', type=int, default=1, help='Number of iterations')
parser.add_argument('--directory', '-d', type=str, help='Output directory for district plans')

args = parser.parse_args()

def grow_graph(graph, district_count):
    '''
    '''
    start_time = time.time()
    node_count = len(graph.nodes())
    node_indexes = numpy.array(range(node_count))

    districts = range(1, 1+district_count)
    max_iterations = int(math.pow(node_count, 1.5))
    iterations = numpy.zeros((max_iterations, node_count), int)

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
            raise ValueError('Out of room')

    end_time = time.time()
    district_map = iterations[-1,:]

    print('done in {:.3f} seconds'.format(end_time - start_time), file=sys.stderr)
    
    return district_map

graph = networkx.readwrite.read_edgelist(args.graph_path, nodetype=int)
print('{} nodes into {} districts'.format(len(graph.nodes()), args.district_count), file=sys.stderr)

for i in range(args.iterations):
    district_map = grow_graph(graph, args.district_count)
    district_str = ' '.join(list(map(str, district_map)))
    
    if args.directory:
        map_str = ''.join([chr(d) for d in district_map])
        map_hash = hashlib.sha1(map_str.encode('utf8')).hexdigest()
        map_path = os.path.join(args.directory, map_hash[:2], map_hash[2:4], map_hash[4:]+'.txt')
        if not os.path.isdir(os.path.dirname(map_path)):
            os.makedirs(os.path.dirname(map_path))
        with open(map_path, 'w') as file:
            print(district_str, file=file)
    else:
        print(district_str, file=sys.stdout)
