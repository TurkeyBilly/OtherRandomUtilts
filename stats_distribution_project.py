import itertools as it
import statistics
from typing import TypeVar
import matplotlib.pyplot as plt

_T = TypeVar("_T")
def list_count(items: list[_T]) -> dict[_T, int]:
    counts = dict()
    for i in items:
        counts[i] = counts.get(i, 0) + 1
    return counts

def round_dict(d: dict, n=3) -> dict:
    res = dict()
    for key in d:
        res[key] = round(d[key], n)
    return res

def combine_dict(key_: list[_T], item_: list[_T]) -> dict[_T, _T]:
    d = {}
    assert len(key_)==len(item_)
    for i in range(len(key_)):
        if d.get(key_[i], None) is None:
            d[key_[i]] = item_[i]
        else:
            d[key_[i]] += item_[i]
    return round_dict(d)

def product(items: list[float]) -> float:
    cnt = 1
    for i in items:
        cnt *= i
    return cnt

value = [15, 16, 17, 18]
prob = [0.1, 0.2, 0.3, 0.4]

mean_val, median_val, prob_dis = [], [], []
for v, p in zip(it.product(value, repeat=3), it.product(prob, repeat=3)):
    mean_val.append(round(sum(v) / 3, 3))
    prob_dis.append(round(product(p), 3))
    median_val.append(round(statistics.median(v), 3))
    

print(combine_dict(mean_val, prob_dis))
print(combine_dict(median_val, prob_dis))
