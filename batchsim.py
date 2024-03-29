#!/usr/bin/python3

import random
import math
import matplotlib
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
from statistics import mean

NUM_BLOCK_SIM = 100000

contributors_save_file = open('contributors-dump.json', 'r')
service_nodes = json.load(contributors_save_file)

# Counts the number of outputs that our list would result in if payed out every block (no change)
count_default = 0

for block in range(NUM_BLOCK_SIM):
    count_default = count_default + len(service_nodes[block % len(service_nodes)])

print("Outputs without batching: {}".format(count_default))

# Simulates only paying out every batchsize
def sim(batchsize):
    count_batched = 0
    max_block_size = 0
    batched = {}

    for block in range(NUM_BLOCK_SIM):
        blockoutputs = 0
        # creates a list of contributors to payout in pop_addresses
        pop_addresses = []
        for address in batched:
            if batched[address] < block - batchsize:
                count_batched = count_batched + 1
                blockoutputs = blockoutputs + 1
                pop_addresses.append(address)

        # deleting as if they were paid
        for address in pop_addresses:
            batched.pop(address)

        # checking how big the outputs of a transaction will get
        if blockoutputs > max_block_size:
            max_block_size = blockoutputs

        # adds to the list if the reward winners are not already due for payments
        for address in service_nodes[block % len(service_nodes)]:
            if address not in batched:
                batched.update({address: block})

    # Compare to the no change case
    savings = (count_default - count_batched) / count_default
    # print("Outputs with batching: {}".format(count_batched))
    # print("Savings in number Outputs: {:.2%}".format(savings))
    # print("max block size: {}".format(max_block_size))
    return savings, max_block_size


savings_y1 = []
savings_y2 = []
savings_x = []

for block in tqdm(range(1, math.ceil(7500/20))):
    granularity = 20
    y1, y2 = sim(block * granularity)
    savings_y1.append(y1)
    savings_y2.append(y2)
    savings_x.append(block * granularity)


fig, axes = plt.subplots(nrows=2)

axes[0].plot(savings_x, savings_y1, label = "Savings %")
axes[0].set_ylabel("Savings %")

axes[1].plot(savings_x, savings_y2, label = "Outputs #")
axes[1].set_ylabel("Outputs #")

plt.savefig("batched_savings.png", bbox_inches="tight")
