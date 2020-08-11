import pickledb
import matplotlib.pyplot as plt
import sys

experiments = {
    'DSA_1': [4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_2': [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_3': [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_4': [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_5': [6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_6': [6, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_7': [6, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_8': [6, 4, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_9': [6, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'DSA_10': [6, 4, 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'MGM_1': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    'MGM_2': [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'MGM_3': [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'MGM_4': [4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    'MGM_5': [6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'MGM_6': [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    'MGM_7': [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    'MGM_8': [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    'MGM_9': [6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'MGM_10': [6, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
}

DSA_avg = []
MGM_avg = []
last_DSA = []
last_MGM = []


for i in range(15):
    DSA_sum = 0.0
    MGM_sum = 0.0
    for j in range(1, 11):
        DSA_sum += experiments.get('DSA_%s' % j)[i]
        MGM_sum += experiments.get('MGM_%s' % j)[i]
    DSA_avg.append(DSA_sum/10)
    MGM_avg.append(MGM_sum/10)

print DSA_avg
print MGM_avg

for i in range(1, 11):
    last_DSA.append(experiments.get('DSA_%s' % i)[14])
    last_MGM.append(experiments.get('MGM_%s' % i)[14])

print last_DSA, last_MGM

from scipy import stats
# x = stats.norm.rvs(loc=5, scale=3, size=100)
# #print x
# print stats.shapiro(x)
#
# #stats.shapiro(last_DSA)
# print stats.shapiro(last_MGM)

print stats.ttest_ind(last_DSA,last_MGM)
# plt.plot(x, DSA_avg, 'r', x, MGM_avg, 'g')
# plt.ylim(-1, 5)
# plt.xlabel('Iteration')
# plt.ylabel('Average cost (per 10 problems)')
# plt.title('DSA vs MGM')
# plt.text(11, 4,'Red -> DSA \nGreen -> MGM')
# plt.show()
