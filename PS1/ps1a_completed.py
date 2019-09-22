###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cows = {}
    with open(filename) as f:
        for line in f:
            # strip new line characters and split by commas
            (name, weight) = line.rstrip().split(',')
            if name not in cows:
                # convert weight to int and store in cows dictionary
                cows[name] = int(weight)

    return cows



# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # created list of cows sorted by weight descending
    sorted_cows = sorted(cows.items(), key = lambda x:x[1], reverse=True)

    # init list of chartered shuttles
    shuttles = []

    # keep going to all cows are chartered on a shuttle!
    while sorted_cows:
        # init list of cows on current shuttle and set shuttle space limit
        this_shuttle = []
        space_left = limit
        for i in range(len(sorted_cows)):
            # take heaviest cow in list
            (name, weight) = sorted_cows.pop(0)
            # try to fit on shuttle
            if weight <= space_left:
                this_shuttle.append(name)
                space_left -= weight
            # else put back into queue
            else:
                sorted_cows.append((name, weight))
        
        # if shuttle has cargo, add to transport charter
        if this_shuttle:
            shuttles.append(this_shuttle)

    return shuttles
            


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # init least number of shuttles based on having one cow in each shuttle
    # (worst case scenario)
    least_shuttles = len(cows)
    shuttles = [[cow] for cow in cows.keys()]
    # init generator to enumerate all possible shuttle partitionings
    partitionings = get_partitions(cows)
    # check weight of each partition in each partitioning
    for partition in partitionings:
        # get number of shuttles in partition
        nb_shuttles = len(partition)
        # if not better than current best number, skip to next partition
        if nb_shuttles >= least_shuttles:
            continue
        # check all shuttles meet weight requirements
        limit_exceeded = False
        for shuttle in partition:
            # sum weight of all cows in shuttle
            shuttle_weight = sum([cows[name] for name in shuttle])
            # if weight is over the limit, flag and break out of loop
            if shuttle_weight > limit:
                limit_exceeded = True
                break
        if not limit_exceeded:
            least_shuttles = nb_shuttles
            shuttles = partition

    return shuttles



# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    
    cows = load_cows('ps1_cow_data.txt')

    tic = time.time()
    trips = greedy_cow_transport(cows, limit=10)
    toc = time.time()
    print(f'greedy_cow_transport algo solves for {len(trips)} trips in {toc - tic:.4f} seconds')
    
    tic = time.time()
    trips = brute_force_cow_transport(cows, limit=10)
    toc = time.time()
    print(f'greedy_cow_transport algo solves for {len(trips)} trips in {toc - tic:.4f} seconds')

    return