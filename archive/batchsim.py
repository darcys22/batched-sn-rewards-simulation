#!/usr/bin/python3

import random
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm


SERVICE_NODE_COUNT = 1700
UNIQUE_ADDRESSES = 1200
NUM_BLOCK_SIM = 100000

service_nodes = []
# node has random number of contributors, higher prob of 1 and 4 will make a list as long as SERVICE_NODE_COUNT
# contributors_each_node is a list of number of contributers for each SN
contributors_each_node = random.choices(
    population=[1, 2, 3, 4], weights=[0.4, 0.1, 0.1, 0.4], k=SERVICE_NODE_COUNT
)

# Iterate the list of number of contributors and the ID of a contributor to that SN
# so we have our service_nodes list being a list of contributors for each SN
for service_node in contributors_each_node:
    contributors_arr = []
    for contributors in range(service_node):
        node = random.randint(0, UNIQUE_ADDRESSES)
        contributors_arr.append(node)
    service_nodes.append(contributors_arr)

# print(service_nodes)

# Counts the number of outputs that our list would result in if payed out every block (no change)
count_default = 0

for block in range(NUM_BLOCK_SIM):
    count_default = count_default + len(service_nodes[block % UNIQUE_ADDRESSES])

print("Outputs without batching: {}".format(count_default))

# Simulates only paying out every batchsize
def sim(batchsize):
    count_batched = 0
    batched = []

    for block in range(NUM_BLOCK_SIM):
        # creates a list of contributors to payout
        batched = batched + service_nodes[block % UNIQUE_ADDRESSES]
        if block % batchsize == 0:
            # Pays out once per unique address in the list of contributors created above
            count_batched = count_batched + len(set(batched))
            batched = []

    # Compare to the no change case
    savings = (count_default - count_batched) / count_default
    # print("Outputs with batching: {}".format(count_batched))
    # print("Savings in number Outputs: {:.2%}".format(savings))
    return savings


savings_y = []
savings_x = []

for block in tqdm(range(1, 100)):
    savings_y.append(sim(block * 50))
    savings_x.append(block * 50)


plt.plot(savings_x, savings_y)
plt.ylabel("Savings %")
plt.savefig("batched_savings.png", bbox_inches="tight")
