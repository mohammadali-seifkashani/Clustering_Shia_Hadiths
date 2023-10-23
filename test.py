import re
import numpy as np
from utils import load_json, save_json


def survey(clusters, noor):
    clusterslens = np.array([len(c) for c in clusters])
    noorlens = np.array([len(n) for n in noor])

    print('len(mcm65):', len(clusterslens))
    print('len(noor):', len(noorlens))

    print('mean_cluster_length(mcm65):', np.mean(clusterslens))
    print('mean_cluster_length(noor):', np.mean(noorlens))

    print('max_cluster_length(mcm65):', np.max(clusterslens))
    print('max_cluster_length(noor):', np.max(noorlens))

    print('variance(mcm65):', np.var(clusterslens))
    print('variance(noor):', np.var(noorlens))


myclustering = load_json('results/maxcommonmax65_texts.json')
noor = load_json('check/noor_automatic.json')
survey(myclustering, noor)






# for key, value in data.items():
#     if len(value.split()) < 5:
#         continue
#     rj = requests.post('https://hadith.ai/sadr/', headers={'accept': 'application/json', 'Content-Type': 'application/json'}, json={'query': value})
#     print(rj.json())
#     print()


# from difflib import SequenceMatcher
#
# a = "dsa jld lal"
# b = "dsajld kll"
# c = "dsc jle kal"
# d = "dsd jlekal"
#
# ss = [a,b,c,d]
#
# s = SequenceMatcher()
#
# for i in range(len(ss)):
#     x = ss[i]
#     s.set_seq1(x)
#     for j in range(i+1,len(ss)):
#
#         y = ss[j]
#         s.set_seq2(y)
#
#         print()
#         print(s.ratio())
#         print(s.get_matching_blocks())
