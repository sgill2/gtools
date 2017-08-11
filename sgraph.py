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

def addGraph(file_names, fig, colors, gtype='dev'):
    if isinstance(gtype, str):
        gtype = [gtype]
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
            print(len(numbers))
            print(fi)
            a_list.append(accept/(float(len(numbers))))
            step_name = float(os.path.basename(fi).split('stats_')[1].split('.txt')[0])
            step_list.append(step_name)
            mean = np.mean(numbers)
            mean_list.append(mean)
            dev = np.std(numbers)
            dev_list.append(dev)
    num_plots = len(gtype)

    for ty in gtype:
        if ty not in ['accept', 'dev', 'avg']:
            raise ValueError
    counter = 1
    #colors = itertools.cycle(['r', 'b', 'g', 'black', 'orange'])
    color_choice = colors.next()
    for ty in gtype:
        ax = fig.add_subplot(num_plots,1,counter)
        counter = counter+1
        if ty == 'accept':
            line = ax.scatter(step_list, a_list, color=color_choice, label=name)
            ax.set_ylabel('Acceptance Ratio')
            ax.set_title('Acceptance Vs NCMC steps')
        elif ty == 'dev':
            ax.set_ylabel('Std Dev (-kT)')
            ax.set_title('Protocol work Std Dev vs NCMC steps')
            print('dev list', dev_list)
            line = ax.scatter(step_list, dev_list, color=color_choice, label=name)
        elif ty == 'avg':
            ax.set_ylabel('Average (-kT)')
            ax.set_title('Protocol work Avg vs NCMC steps')
            line = ax.scatter(step_list, mean_list, color=color_choice, label=name)

    return line


def makeGraph(glob_name='stats*.txt', gtype='dev', show=True, save=True, out_prefix='temp'):
    if isinstance(gtype, str):
        gtype = [gtype]

    colors = itertools.cycle(['r', 'b', 'g', 'black', 'orange'])

    fig = plt.figure(figsize=(10,8))
    #       plt.ylabel('Accept Ratio')

#    fig = plt.figure()
#    plt.xlabel('NCMC steps')
    if gtype == 'accept':
        pass
 #       plt.ylabel('Accept Ratio')
 #       plt.title('Accept Ratio vs NCMC Steps')
    elif gtype == 'dev':
        pass

 #       plt.ylabel('Protocol Work Std Dev\n (-kT)')
 #       plt.title('Protocol Work Std Dev vs NCMC Steps')
    elif gtype == 'avg':
        pass

 #       plt.ylabel('Protocol Work Average\n (-kT)')
 #       plt.title('Protocol Work Average vs NCMC Steps')

    files = glob_files(glob_name)
    dirs = [x[0] for x in os.walk('./')][1:]
    for di in dirs:
        files = glob_files(os.path.join(di, glob_name))
        addGraph(files, fig, colors, gtype=gtype)
        for fi in files:
            numbers, accept, nans = getStats(fi)
    print(dirs)
    plt.legend(fancybox=True, framealpha=0.5)
    axlast = fig.get_axes()[-1]
    axlast.set_xlabel('steps NCMC')
    if len(gtype) > 1:
        out_name = out_prefix + '.png'
    else:
        out_name = out_prefix + '_'+gtype[0]+'.png'
    if save == True:
        plt.savefig(out_name)
    if show == True:
        plt.show()
    return fig
#for index, i in enumerate(['dev', 'avg', 'accept']):
#    fig = makeGraph(gtype=i, show=False, out_prefix='tolwater')

fig = makeGraph(gtype=['dev', 'accept'], show=True, save=True, out_prefix='tollys')





