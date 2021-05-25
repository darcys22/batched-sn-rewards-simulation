#!/usr/bin/python3

import random
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
    batched = []
    batch_outputs = []

    for block in range(NUM_BLOCK_SIM):
        # creates a list of contributors to payout
        batched = batched + service_nodes[block % len(service_nodes)]
        if block % batchsize == 0:
            # Pays out once per unique address in the list of contributors created above
            count_batched = count_batched + len(set(batched))
            batch_outputs.append(len(set(batched)))
            batched = []

    # Compare to the no change case
    savings = (count_default - count_batched) / count_default
    # print("Outputs with batching: {}".format(count_batched))
    # print("Savings in number Outputs: {:.2%}".format(savings))
    return savings, mean(batch_outputs)


savings_y1 = []
savings_y2 = []
savings_x = []

for block in tqdm(range(1, 10)):
    granularity = 200
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
