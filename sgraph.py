"""Graphs BLUES stats files"""

import matplotlib.pyplot as plt
import glob
import math
import numpy as np
import os
from cycler import cycler
import itertools

def glob_files(file_name):
    files = sorted(glob.glob(file_name))
    step_list = [int(j.split('_')[1].split('.')[0]) for j in files]
    sort_list = [b[0] for b in sorted(enumerate(step_list), key=lambda i:i[1])]
    files = [files[i] for i in sort_list]
    return files

def getStats(file_name):
    numbers = []
    accept = 0
    nans = 0

    with open(file_name, 'r') as f:
        a = f.readlines()
    for line in a:
        try:
            split = line.split()
            if split[2] == 'ACCEPTED:':
                accept = accept+1
                if split[0] == 'NCMC':
                    numbers.append(float(split[4]))
            if split[2] == 'REJECTED:':
                if split[3] == 'nan':
                    nans = nans+1
                else:
                    numbers.append(float(split[3]))
        except IndexError:
            pass
    return numbers, accept, nans

def addGraph(file_names, fig, colors, type='dev'):
    name = os.path.basename(os.path.abspath(os.path.join(file_names[0], os.pardir)))
    print(name)
    n_list = []
    a_list = []
    mean_list = []
    step_list = []
    dev_list = []
    for fi in file_names:
        numbers, accept, nans = getStats(fi)
        if len(numbers) > 0:
            n_list.append(numbers)
            print(len(numbers))
            print(fi)
            a_list.append(accept/(float(len(numbers))))
            step_name = float(os.path.basename(fi).split('stats_')[1].split('.txt')[0])
            step_list.append(step_name)
            mean = np.mean(n_list)
            mean_list.append(mean)
            dev = np.std(n_list)
            dev_list.append(dev)


    ax = fig.add_subplot(111)
    if type == 'accept':
        line = ax.scatter(step_list, a_list, color=next(colors), label=name)
    elif type == 'dev':
        line = ax.scatter(step_list, dev_list, color=next(colors), label=name)
    elif type == 'avg':
        line = ax.scatter(step_list, mean_list, color=next(colors), label=name)
    return line


def makeGraph(glob_name='stats*.txt', gtype='dev'):
    colors = itertools.cycle(['r', 'b', 'g'])

    fig = plt.figure()
    files = glob_files(glob_name)
    dirs = [x[0] for x in os.walk('./')][1:]
    for di in dirs:
        files = glob_files(os.path.join(di, glob_name))
        addGraph(files, fig, colors, type=gtype)
        for fi in files:
            numbers, accept, nans = getStats(fi)
    print(dirs)
    plt.legend()
    plt.show()

makeGraph()


colors = itertools.cycle(['r', 'b', 'g'])
plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +
                           cycler('linestyle', ['-', '--', ':', '-.'])))

fig = plt.figure()
files = glob_files('stats*.txt')
dirs = [x[0] for x in os.walk('./')][1:]
for di in dirs:
    files = glob_files(os.path.join(di, 'stats*.txt'))
    addGraph(files, fig, colors, type='dev')
    for fi in files:
        numbers, accept, nans = getStats(fi)
print(dirs)
plt.legend()
plt.show()
gmax = None
gmin = None
def getStats(file_name):
    numbers = []
    accept = 0
    nans = 0

    with open(file_name, 'r') as f:
        a = f.readlines()
    for line in a:
        try:
            split = line.split()
            if split[2] == 'ACCEPTED:':
                accept = accept+1
                if split[0] == 'NCMC':
                    numbers.append(float(split[4]))
            if split[2] == 'REJECTED:':
                if split[3] == 'nan':
                    nans = nans+1
                else:
                    numbers.append(float(split[3]))
        except IndexError:
            pass
    return numbers, accept, nans
entries = math.ceil(math.sqrt(float(len(files))))
if 1:
    gmax = 10
    gmin = -50
for i, item in enumerate(files):
    numbers, accept, nans = getStats(item)
    total_entries = float(nans + len(numbers))
    if gmax is not None:
        numbers = [j for j in numbers if j <=gmax and j >=gmin]
    plot_num = i+1
    ax1 = plt.subplot(entries,entries,plot_num)
    accept = float(accept)
    if len(numbers) > 0:
        ax1.hist(numbers, 50, normed=1)
        ax1.set_title(item.split('.')[0] + ' ' + 'acc ' + str(round((accept/total_entries),3)) + '\ngraphed ' + str(len(numbers)) + ' total ' + str(total_entries) + ' nan ' + str(nans))

#ax1.set_xlim([-20,10])
    if gmax is not None:
        ax1.set_xlim([gmin,gmax])
#plt.tight_layout()
#plt.show()
