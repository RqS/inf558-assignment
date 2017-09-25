import json
import sys
import random
import re

with open(sys.argv[1]) as d:
    data = json.load(d)

train_N = int(sys.argv[2])
test_N = int(sys.argv[3])

idx = random.sample(range(len(data)), train_N + test_N + 1)
train_idx = idx[:train_N]
test_idx = idx[train_N+1:]

train_text = [data[train_idx[i]]["Summery"].replace("\n", " ").strip().encode("utf-8") for i in range(train_N) if data[train_idx[i]]["Summery"]]

test_text = [data[test_idx[i]]["Summery"].replace("\n", " ").strip().encode("utf-8") for i in range(test_N) if data[test_idx[i]]["Summery"]]

train_f = open("train.txt", "w")
for i in train_text:
    train_f.write(re.sub(' +', ' ', i))
    train_f.write("\n")

train_f.close()

test_f = open("test.txt", "w")
for i in test_text:
    test_f.write(re.sub(' +', ' ', i))
    test_f.write("\n")

test_f.close()