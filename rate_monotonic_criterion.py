# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 18:39:55 2018

@author: Madhu
"""

from math import gcd
from functools import reduce

print("Enter the number of tasks: ")
n = int(input())

#Calculating the Rate Monotonic Criterion
rm_criterion = n*(pow(2,1/n)-1)

exec_times = []
periodicity = []
cpu_utilization = 0
priorities = [0]*n
ready = []

#Getting the inputs of execution times and periodicities
#While calculating the CPU Utilization
for i in range(n):
    print("Enter execution time of task " + str((i+1)))
    exec_times.append(int(input()))
    
    print("Periodicity of task " + str((i+1)))
    periodicity.append(int(input()))
    
    cpu_utilization += 1/(exec_times[i]*periodicity[i])
    
#Finding total no of clock cycles
total_cc = reduce(lambda a,b: a*b//gcd(a,b), periodicity)

#Initialising the Execution Trace
trace = [[0 for x in range(total_cc)] for y in range(n)]
    
#Testing the problem for Rate Monotonic Criterion
if cpu_utilization <= rm_criterion:
    print("The problem is guaranteed to be schedulable")
else:
    print("The problem may or may not be schedulable")

#Making a list of tasks ordered from highest priority to lowest    
test = periodicity.copy()
count = 1

while(test):
    mini = min(test)
    test.remove(mini)
    priorities[periodicity.index(mini)]=count
    count+=1

#Creating dictionaries of priorities and execution times matched with tasks
tasks = list(i for i in range(1,n+1))
dict_priorities = dict(zip(tasks, priorities))
dict_exec_times = dict(zip(tasks, exec_times))    

#Initialising the ready queue
for j in range(len(periodicity)):
    for k in range(dict_exec_times[j+1]):
        ready.append(j+1)

#Performing the Scheduling task
#Updating the Ready Queue
for i in range(total_cc):
    if i>2:
        for j in range(len(periodicity)):
            if i%periodicity[j] == 0:
                if (j+1) not in ready:
                    for k in range(dict_exec_times[j+1]):
                        ready.append(j+1)
    #Getting the task with highest priority from the Ready Queue
    highest=n+1
    if(ready):
        for j in ready:
            if dict_priorities[j] < highest:
                highest = dict_priorities[j]
    else:
        continue
    
    #Setting the respective task for execution and removing it from the ready queue
    for task, priority in dict_priorities.items():
        if priority == highest:
            executed_task = task
            trace[task-1][i] = 1
            ready.remove(task)
            
#Printing the execution trace
import matplotlib.pyplot as plt

#Setting the x axis
xax=[]
axx=[]
for q in range(total_cc):
    xax.append(q)
    axx.append(q)
axx.append(total_cc)

#Initialising the bar plots
ynos = []
ylabels = ['Tasks']
ylegend = []

for i in range(n):
    plt.bar(xax, trace[i], bottom = i, align='edge', width = 1)
    ynos.append(i)
    ylabels.append('Task ' + str(i+1))
    ylegend.append('Task ' + str(i+1))
    
ynos.append(i+1)

plt.xticks(axx)
plt.yticks(ynos, ylabels)
plt.legend(ylegend)
    
plt.grid()        
plt.show()

